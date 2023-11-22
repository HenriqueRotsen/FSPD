import sys
import grpc
import centralizer_pb2, centralizer_pb2_grpc
import storage_pb2, storage_pb2_grpc

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
    with grpc.insecure_channel(f'localhost:{sys.argv[1]}') as channel:
        while True:
            parts = input().strip().split(',')

            if parts[0] == 'C':
                key = int(parts[1])
                identifier = map_key(channel, key)
                print(f"Identificador associado à chave {key}: {identifier}")
            elif parts[0] == 'T':
                num_keys = terminate(channel)
                print(num_keys)
                break
            else:
                print("Comando inválido. Tente novamente.")

if __name__ == '__main__':
    main()
