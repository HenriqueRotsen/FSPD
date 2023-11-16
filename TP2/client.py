import grpc
import storage_pb2
import storage_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = storage_pb2_grpc.KeyValueStoreStub(channel)

    while True:
        command = input("Digite um comando (I, C, A, T): ").strip().split(',')

        if command[0] == 'I':
            key = int(command[1])
            value = command[2]
            request = storage_pb2.KeyValueRequest(key=key, value=value)
            response = stub.Insert(request)
            print(f"Resultado da inserção: {response.result}")

        elif command[0] == 'C':
            key = int(command[1])
            request = storage_pb2.KeyRequest(key=key)
            response = stub.Consult(request)
            print(f"Valor associado à chave: {response.value}")

        elif command[0] == 'A':
            service_identifier = command[1]
            request = storage_pb2.ActivationRequest(service_identifier=service_identifier)
            response = stub.Activate(request)
            print(f"Resultado da ativação: {response.result}")

        elif command[0] == 'T':
            request = storage_pb2.EmptyRequest()
            response = stub.Terminate(request)
            print(f"Resultado do término: {response.result}")
            break

if __name__ == '__main__':
    run()
