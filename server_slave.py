import logging
import operator
import time
from concurrent import futures
from threading import Thread

import grpc

import calculator_pb2
import calculator_pb2_grpc

# Settings
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
ADDRESS_SERVER_SLAVE_1 = 'localhost:50052'
ADDRESS_SERVER_SLAVE_2 = 'localhost:50053'

SLAVE_1_OPERATIONS = {
    '*': operator.mul,
    '/': operator.truediv,
}

SLAVE_2_OPERATIONS = {
    '**': operator.pow
}


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

    # Start first server slave
    thread = Thread(target=start_server_slave, args=(ADDRESS_SERVER_SLAVE_1, SLAVE_1_OPERATIONS))
    thread.start()

    # Start second server slave node
    start_server_slave(ADDRESS_SERVER_SLAVE_2, SLAVE_2_OPERATIONS)
