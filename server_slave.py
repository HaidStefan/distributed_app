import logging
import operator
import time
from concurrent import futures
from threading import Thread

import grpc

import calculator_pb2
import calculator_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CalculatorSlave(calculator_pb2_grpc.CalculatorSlaveServicer):

    def __init__(self, operations):
        super().__init__()
        self.operations = operations

    def DoOperation(self, request, context):
        result = self.operations[request.op](request.a, request.b)
        return calculator_pb2.OperationResponse(result=result, error=False)


def start_server_slave(address, operations):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorSlaveServicer_to_server(CalculatorSlave(operations=operations), server)
    server.add_insecure_port(address)
    server.start()
    print("Server Slave started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()

    slave1_operations = {
        '*': operator.mul,
        '/': operator.truediv,
    }

    slave2_operations = {
        '**': operator.pow
    }

    thread = Thread(target=start_server_slave, args=('localhost:50052', slave1_operations))
    thread.start()

    start_server_slave('localhost:50053', slave2_operations)
