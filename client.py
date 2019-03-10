from __future__ import print_function
import logging

import grpc

import calculator_pb2
import calculator_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        response = stub.Calculate(calculator_pb2.CalculationRequest(expression="99*99"))
    print("Response from calculator: " + str(response.result))


if __name__ == '__main__':
    logging.basicConfig()
    run()
