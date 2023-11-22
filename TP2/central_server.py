from concurrent import futures
import sys
import grpc
import threading
import centralizer_pb2, centralizer_pb2_grpc

class CentralizerServicer(centralizer_pb2_grpc.CentralizerServicer):
    def __init__(self, stop_event):
        self.key_directory = {}
        self._stop_event = stop_event

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
        self._stop_event.set()
        return centralizer_pb2.RegisterResponse(num_keys= len(self.key_directory.keys()))

def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    centralizer_pb2_grpc.add_CentralizerServicer_to_server(CentralizerServicer(stop_event), server)
    port = sys.argv[1]
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    stop_event.wait()
    server.stop(grace=None)

if __name__ == '__main__':
    serve()
