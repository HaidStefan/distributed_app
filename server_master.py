import logging
import time
from concurrent import futures

import grpc

import calculator_pb2
import calculator_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CalculatorMaster(calculator_pb2_grpc.CalculatorServicer):

    def Calculate(self, request, context):
        print("Received: " + request.expression)
        expr = request.expression

        response = calculator_pb2.CalculationResponse(result=99, error=False)

        return response


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
