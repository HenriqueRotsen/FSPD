# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import centralizer_pb2 as centralizer__pb2


class CentralizerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/Centralizer/Register',
                request_serializer=centralizer__pb2.RegisterRequest.SerializeToString,
                response_deserializer=centralizer__pb2.RegisterResponse.FromString,
                )
        self.MapKey = channel.unary_unary(
                '/Centralizer/MapKey',
                request_serializer=centralizer__pb2.MapKeyRequest.SerializeToString,
                response_deserializer=centralizer__pb2.MapKeyResponse.FromString,
                )
        self.Terminate = channel.unary_unary(
                '/Centralizer/Terminate',
                request_serializer=centralizer__pb2.TerminateRequest.SerializeToString,
                response_deserializer=centralizer__pb2.RegisterResponse.FromString,
                )


class CentralizerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MapKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Terminate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CentralizerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=centralizer__pb2.RegisterRequest.FromString,
                    response_serializer=centralizer__pb2.RegisterResponse.SerializeToString,
            ),
            'MapKey': grpc.unary_unary_rpc_method_handler(
                    servicer.MapKey,
                    request_deserializer=centralizer__pb2.MapKeyRequest.FromString,
                    response_serializer=centralizer__pb2.MapKeyResponse.SerializeToString,
            ),
            'Terminate': grpc.unary_unary_rpc_method_handler(
                    servicer.Terminate,
                    request_deserializer=centralizer__pb2.TerminateRequest.FromString,
                    response_serializer=centralizer__pb2.RegisterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Centralizer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Centralizer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Centralizer/Register',
            centralizer__pb2.RegisterRequest.SerializeToString,
            centralizer__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MapKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Centralizer/MapKey',
            centralizer__pb2.MapKeyRequest.SerializeToString,
            centralizer__pb2.MapKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Terminate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Centralizer/Terminate',
            centralizer__pb2.TerminateRequest.SerializeToString,
            centralizer__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)