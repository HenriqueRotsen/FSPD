import grpc
from concurrent import futures
import centralizer_pb2
import centralizer_pb2_grpc

class CentralizerServicer(centralizer_pb2_grpc.CentralizerServicer):
    def __init__(self):
        self.key_directory = {}

    def Register(self, request, context):
        identifier = request.identifier
        keys = request.keys

        # Tratamento de colisões: Sobrescreve a associação se a chave já estiver registrada
        for key in keys:
            self.key_directory[key] = identifier

        return centralizer_pb2.RegisterResponse(num_keys=len(keys))

    def MapKey(self, request, context):
        key = request.key
        identifier = self.key_directory.get(key, '')
        return centralizer_pb2.MapKeyResponse(identifier=identifier)

    def Terminate(self, request, context):
        num_keys = len(self.key_directory)
        context.abort()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    centralizer_pb2_grpc.add_CentralizerServicer_to_server(CentralizerServicer(), server)
    port = 50052  # Defina a porta desejada para o servidor centralizador
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'Servidor Centralizador iniciado na porta {port}')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
