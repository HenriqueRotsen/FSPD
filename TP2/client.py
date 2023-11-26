import sys
import grpc
import storage_pb2
import storage_pb2_grpc

def run():
    # Efetua a conexao com o servidor
    channel = grpc.insecure_channel(sys.argv[1])
    stub = storage_pb2_grpc.KeyValueStoreStub(channel)

    while True:
        # Separa as entradas
        command = input().strip().split(',')

        # Realiza a insercao
        if command[0] == 'I':
            key = int(command[1])
            value = command[2]
            request = storage_pb2.KeyValueRequest(key=key, value=value)
            response = stub.Insert(request)
            print(response.result)

        # Realiza a consulta
        elif command[0] == 'C':
            key = int(command[1])
            request = storage_pb2.KeyRequest(key=key)
            response = stub.Consult(request)
            print(response.value)

        # Realiza a ativacao (so funciona se rodar o servidor com a flag)
        elif command[0] == 'A':
            server_ip = command[1]
            request = storage_pb2.ActivationRequest(service_identifier=server_ip)
            response = stub.Activate(storage_pb2.ActivationRequest(service_identifier=server_ip))
            print(response.result)

        # Termina o programa
        elif command[0] == 'T':
            request = storage_pb2.TerminateRequest()
            response = stub.Terminate(request)
            print(response.result)
            break

if __name__ == '__main__':
    run()
