# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import seller_pb2 as seller__pb2


class SellerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Seller_Notification = channel.unary_unary(
                '/Seller/Seller_Notification',
                request_serializer=seller__pb2.NotifyClientRequest.SerializeToString,
                response_deserializer=seller__pb2.Void.FromString,
                )


class SellerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Seller_Notification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SellerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Seller_Notification': grpc.unary_unary_rpc_method_handler(
                    servicer.Seller_Notification,
                    request_deserializer=seller__pb2.NotifyClientRequest.FromString,
                    response_serializer=seller__pb2.Void.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Seller', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Seller(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Seller_Notification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Seller/Seller_Notification',
            seller__pb2.NotifyClientRequest.SerializeToString,
            seller__pb2.Void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
