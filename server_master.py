import logging
import time
from concurrent import futures
import ast
import operator
import grpc
import calculator_pb2
import calculator_pb2_grpc

# Settings
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
ADDRESS_SERVER_MASTER = 'localhost:50051'
ADDRESS_SERVER_SLAVE_1 = 'localhost:50052'
ADDRESS_SERVER_SLAVE_2 = 'localhost:50053'


class CalculatorMaster(calculator_pb2_grpc.CalculatorServicer):

    def Calculate(self, request, context):
        try:
            result = self.arithmetic_eval(request.expression)
            return calculator_pb2.CalculationResponse(result=result, status=calculator_pb2.CalculationResponse.SUCCESS)

        except ZeroDivisionError:
            return calculator_pb2.CalculationResponse(result=None,
                                                      status=calculator_pb2.CalculationResponse.ZERO_DIVISION_ERROR)
        except Exception:
            return calculator_pb2.CalculationResponse(result=None,
                                                      status=calculator_pb2.CalculationResponse.INVALID_FORMAT_ERROR)

    @staticmethod
    def arithmetic_eval(s):
        root_node = ast.parse(s, mode='eval')

        # available operations
        bin_options = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: stub_mul,
            ast.Div: stub_div,
            ast.Pow: stub_pow
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                try:
                    return bin_options[type(node.op)](_eval(node.left), _eval(node.right))
                except ZeroDivisionError:  # pass exception of dividing by 0
                    raise
            else:
                raise Exception('Unsupported type {}'.format(node))

        return _eval(root_node.body)


def stub_mul(a, b): return do_operation_on_stub(a, '*', b, ADDRESS_SERVER_SLAVE_1)


def stub_div(a, b):
    if b == 0:
        raise ZeroDivisionError
    return do_operation_on_stub(a, '/', b, ADDRESS_SERVER_SLAVE_1)


def stub_pow(a, b): return do_operation_on_stub(a, '**', b, ADDRESS_SERVER_SLAVE_2)


def do_operation_on_stub(a, op, b, address):
    with grpc.insecure_channel(address) as channel:
        stub = calculator_pb2_grpc.CalculatorSlaveStub(channel)
        response = stub.DoOperation(calculator_pb2.OperationRequest(a=a, op=op, b=b))
        return response.result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorMaster(), server)
    server.add_insecure_port(ADDRESS_SERVER_MASTER)
    server.start()
    print("Server Master started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
