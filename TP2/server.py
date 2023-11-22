from ast import arg
import grpc
import threading
import sys
import socket
from concurrent import futures
import storage_pb2, storage_pb2_grpc
import centralizer_pb2, centralizer_pb2_grpc

class KeyValueStoreServicer(storage_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, stop_event):
        self.key_value_store = {}
        self.activation_flag = len(sys.argv) == 3
        self.stop_event = stop_event

    def Insert(self, request, context):
        key = request.key
        value = request.value
        if key not in self.key_value_store:
            self.key_value_store[key] = value
            return storage_pb2.Response(result=0)
        else:
            return storage_pb2.Response(result=-1)

    def Consult(self, request, context):
        key = request.key
        value = self.key_value_store.get(key, "")
        return storage_pb2.Response(result=0, value=value)

    def Activate(self, request, context):
        if self.activation_flag:
            channel = grpc.insecure_channel(request.service_identifier)
            stub = centralizer_pb2_grpc.CentralizerStub(channel)
            response = stub.Register(centralizer_pb2.RegisterRequest(identifier=f'{socket.getfqdn()}:{sys.argv[1]}', keys=self.key_value_store.keys()))
            
            return storage_pb2.Response(result=response.num_keys)
        else:
            return storage_pb2.Response(result=-1)

    def Terminate(self, request, context):
        self.stop_event.set()
        return storage_pb2.Response(result=0)

def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(stop_event), server)
    port = sys.argv[1]
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    stop_event.wait()
    server.stop(grace=None)

if __name__ == '__main__':
    serve()