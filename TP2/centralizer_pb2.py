# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: centralizer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63\x65ntralizer.proto\"3\n\x0fRegisterRequest\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x0c\n\x04keys\x18\x02 \x03(\x05\"$\n\x10RegisterResponse\x12\x10\n\x08num_keys\x18\x01 \x01(\x05\"\x1c\n\rMapKeyRequest\x12\x0b\n\x03key\x18\x01 \x01(\x05\"$\n\x0eMapKeyResponse\x12\x12\n\nidentifier\x18\x01 \x01(\t\"\x12\n\x10TerminateRequest2\x9c\x01\n\x0b\x43\x65ntralizer\x12/\n\x08Register\x12\x10.RegisterRequest\x1a\x11.RegisterResponse\x12)\n\x06MapKey\x12\x0e.MapKeyRequest\x1a\x0f.MapKeyResponse\x12\x31\n\tTerminate\x12\x11.TerminateRequest\x1a\x11.RegisterResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'centralizer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REGISTERREQUEST']._serialized_start=21
  _globals['_REGISTERREQUEST']._serialized_end=72
  _globals['_REGISTERRESPONSE']._serialized_start=74
  _globals['_REGISTERRESPONSE']._serialized_end=110
  _globals['_MAPKEYREQUEST']._serialized_start=112
  _globals['_MAPKEYREQUEST']._serialized_end=140
  _globals['_MAPKEYRESPONSE']._serialized_start=142
  _globals['_MAPKEYRESPONSE']._serialized_end=178
  _globals['_TERMINATEREQUEST']._serialized_start=180
  _globals['_TERMINATEREQUEST']._serialized_end=198
  _globals['_CENTRALIZER']._serialized_start=201
  _globals['_CENTRALIZER']._serialized_end=357
# @@protoc_insertion_point(module_scope)
