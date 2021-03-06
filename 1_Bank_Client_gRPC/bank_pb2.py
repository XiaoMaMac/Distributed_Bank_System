# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bank.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bank.proto',
  package='bank',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nbank.proto\x12\x04\x62\x61nk\"N\n\rclientRequest\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x0f\n\x07\x45ventID\x18\x02 \x01(\x05\x12\x11\n\tInterface\x18\x03 \x01(\t\x12\r\n\x05Money\x18\x04 \x01(\x03\"=\n\x0e\x62ranchResponse\x12\n\n\x02ID\x18\x02 \x01(\x05\x12\x0f\n\x07\x42\x61lance\x18\x01 \x01(\x03\x12\x0e\n\x06Status\x18\x03 \x01(\t\"N\n\rBranchRequest\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x0f\n\x07\x45ventID\x18\x02 \x01(\x05\x12\x11\n\tInterface\x18\x03 \x01(\t\x12\r\n\x05Money\x18\x04 \x01(\x03\"#\n\x0eupdateResponse\x12\x11\n\tBResponse\x18\x01 \x01(\t2z\n\x06\x63reate\x12\x38\n\x0bMsgDelivery\x12\x13.bank.clientRequest\x1a\x14.bank.branchResponse\x12\x36\n\tpropagate\x12\x13.bank.BranchRequest\x1a\x14.bank.updateResponseb\x06proto3'
)




_CLIENTREQUEST = _descriptor.Descriptor(
  name='clientRequest',
  full_name='bank.clientRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='bank.clientRequest.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='EventID', full_name='bank.clientRequest.EventID', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Interface', full_name='bank.clientRequest.Interface', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Money', full_name='bank.clientRequest.Money', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=98,
)


_BRANCHRESPONSE = _descriptor.Descriptor(
  name='branchResponse',
  full_name='bank.branchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='bank.branchResponse.ID', index=0,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Balance', full_name='bank.branchResponse.Balance', index=1,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Status', full_name='bank.branchResponse.Status', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=161,
)


_BRANCHREQUEST = _descriptor.Descriptor(
  name='BranchRequest',
  full_name='bank.BranchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='bank.BranchRequest.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='EventID', full_name='bank.BranchRequest.EventID', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Interface', full_name='bank.BranchRequest.Interface', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Money', full_name='bank.BranchRequest.Money', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=163,
  serialized_end=241,
)


_UPDATERESPONSE = _descriptor.Descriptor(
  name='updateResponse',
  full_name='bank.updateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='BResponse', full_name='bank.updateResponse.BResponse', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=278,
)

DESCRIPTOR.message_types_by_name['clientRequest'] = _CLIENTREQUEST
DESCRIPTOR.message_types_by_name['branchResponse'] = _BRANCHRESPONSE
DESCRIPTOR.message_types_by_name['BranchRequest'] = _BRANCHREQUEST
DESCRIPTOR.message_types_by_name['updateResponse'] = _UPDATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

clientRequest = _reflection.GeneratedProtocolMessageType('clientRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTREQUEST,
  '__module__' : 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.clientRequest)
  })
_sym_db.RegisterMessage(clientRequest)

branchResponse = _reflection.GeneratedProtocolMessageType('branchResponse', (_message.Message,), {
  'DESCRIPTOR' : _BRANCHRESPONSE,
  '__module__' : 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.branchResponse)
  })
_sym_db.RegisterMessage(branchResponse)

BranchRequest = _reflection.GeneratedProtocolMessageType('BranchRequest', (_message.Message,), {
  'DESCRIPTOR' : _BRANCHREQUEST,
  '__module__' : 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.BranchRequest)
  })
_sym_db.RegisterMessage(BranchRequest)

updateResponse = _reflection.GeneratedProtocolMessageType('updateResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATERESPONSE,
  '__module__' : 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.updateResponse)
  })
_sym_db.RegisterMessage(updateResponse)



_CREATE = _descriptor.ServiceDescriptor(
  name='create',
  full_name='bank.create',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=280,
  serialized_end=402,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgDelivery',
    full_name='bank.create.MsgDelivery',
    index=0,
    containing_service=None,
    input_type=_CLIENTREQUEST,
    output_type=_BRANCHRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='propagate',
    full_name='bank.create.propagate',
    index=1,
    containing_service=None,
    input_type=_BRANCHREQUEST,
    output_type=_UPDATERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CREATE)

DESCRIPTOR.services_by_name['create'] = _CREATE

# @@protoc_insertion_point(module_scope)
