import logging
import time
from concurrent import futures
import ast
import operator

import grpc

import calculator_pb2
import calculator_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CalculatorMaster(calculator_pb2_grpc.CalculatorServicer):

    def Calculate(self, request, context):
        result = self.arithmetic_eval(request.expression)
        return calculator_pb2.CalculationResponse(result=result, error=False)

    @staticmethod
    def arithmetic_eval(s):
        root_node = ast.parse(s, mode='eval')

        # available operations
        bin_options = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow
        }

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                return bin_options[type(node.op)](_eval(node.left), _eval(node.right))
            else:
                raise Exception('Unsupported type {}'.format(node))

        return _eval(root_node.body)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorMaster(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
