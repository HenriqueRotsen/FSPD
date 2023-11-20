import grpc
import centralizer_pb2
import centralizer_pb2_grpc

def register(channel, identifier, keys):
    stub = centralizer_pb2_grpc.CentralizerStub(channel)
    response = stub.Register(centralizer_pb2.RegisterRequest(identifier=identifier, keys=keys))
    return response.num_keys

def map_key(channel, key):
    stub = centralizer_pb2_grpc.CentralizerStub(channel)
    response = stub.MapKey(centralizer_pb2.MapKeyRequest(key=key))
    return response.identifier

def terminate(channel):
    stub = centralizer_pb2_grpc.CentralizerStub(channel)
    response = stub.Terminate(centralizer_pb2.TerminateRequest())
    return response.num_keys

def main():
    with grpc.insecure_channel('localhost:50052') as channel:
        while True:
            command = input("Digite um comando (R,identificador,chaves | M,chave | T): ")
            parts = command.split(',')

            if parts[0] == 'R':
                identifier = parts[1]
                keys = list(map(int, parts[2:]))
                num_keys = register(channel, identifier, keys)
                print(f"Total de chaves registradas: {num_keys}")
            elif parts[0] == 'M':
                key = int(parts[1])
                identifier = map_key(channel, key)
                print(f"Identificador associado à chave {key}: {identifier}")
            elif parts[0] == 'T':
                num_keys = terminate(channel)
                print(f"Total de chaves registradas no servidor centralizador: {num_keys}")
                break
            else:
                print("Comando inválido. Tente novamente.")

if __name__ == '__main__':
    main()
