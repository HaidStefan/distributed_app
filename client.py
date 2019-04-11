from __future__ import print_function
import logging
import grpc
import calculator_pb2
import calculator_pb2_grpc

# Settings
ADDRESS_SERVER_MASTER = 'localhost:50051'


def run():
    stop = False
    while not stop:
        usr_in = input("Do a calculation? [y/n]\n")
        if usr_in.lower() == 'n' or usr_in.lower() == 'no':
            stop = True
        else:
            usr_in = input("Please enter term to calculate!\n")

            with grpc.insecure_channel(ADDRESS_SERVER_MASTER) as channel:
                stub = calculator_pb2_grpc.CalculatorStub(channel)
                response = stub.Calculate(calculator_pb2.CalculationRequest(expression=usr_in))

                if response.status == calculator_pb2.CalculationResponse.SUCCESS:
                    print("The result is : " + str(response.result) + '\n')
                elif response.status == calculator_pb2.CalculationResponse.ZERO_DIVISION_ERROR:
                    print("Error: Divide by zero in expression")
                else:
                    print("Invalid format of expression")


if __name__ == '__main__':
    logging.basicConfig()
    run()
