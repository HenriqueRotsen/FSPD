import sys
import grpc
import centralizer_pb2, centralizer_pb2_grpc
import storage_pb2, storage_pb2_grpc

# Acha o IP do servidor que possui a chave
def map_key(channel, key):
    stub = centralizer_pb2_grpc.CentralizerStub(channel)
    response = stub.MapKey(centralizer_pb2.MapKeyRequest(key=key))
    return response.identifier

# Termina o programa
def terminate(channel):
    stub = centralizer_pb2_grpc.CentralizerStub(channel)
    response = stub.Terminate(centralizer_pb2.TerminateRequestCentral())
    return response.num_keys

def main():
    # Conexao inicial
    with grpc.insecure_channel(f'localhost:{sys.argv[1]}') as channel:
        while True:
            parts = input().strip().split(',')

            # Faz a consulta a partir da "key"
            if parts[0] == 'C':
                key = int(parts[1])
                identifier = map_key(channel, key)
                if identifier != "":
                    channel_content = grpc.insecure_channel(identifier)
                    stub_content = storage_pb2_grpc.KeyValueStoreStub(channel_content)
                    
                    # Consulta o valor associado a chave passada, no servidor que armazena ela
                    response_content = stub_content.Consult(storage_pb2.KeyRequest(key=key))
                    print(f'{identifier}:{response_content.value}')
            elif parts[0] == 'T':
                num_keys = terminate(channel)
                print(num_keys)
                break
            else:
                print("Comando inválido. Tente novamente.")

if __name__ == '__main__':
    main()
