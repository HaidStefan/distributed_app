import logging
import time
from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CalculatorSlave(calculator_pb2_grpc.CalculatorSlaveServicer):

    def __init__(self):
        super().__init__()

    def DoOperation(self, request, context):
        print("do opertion called")
        if request.op == '*':
            result = request.a * request.b
            return calculator_pb2.OperationResponse(result=result, error=False)

        if request.op == '/':
            if request.b == 0:
                return calculator_pb2.OperationResponse(result=None, error=True)  # Error div by 0

            result = request.a / request.b
            return calculator_pb2.OperationResponse(result=result, error=False)
        else:
            return calculator_pb2.OperationResponse(result=None, error=True)    # Error


def start_server_slave():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorSlaveServicer_to_server(CalculatorSlave(), server)
    server.add_insecure_port('localhost:50052')
    server.start()
    print("Server Slave started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    start_server_slave()
