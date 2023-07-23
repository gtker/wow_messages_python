import asyncio
import dataclasses
import enum
import struct
import typing

from all import Locale
from version2 import LoginResult
from all import Os
from all import Platform
from version2 import Population
from all import ProtocolVersion
from version2 import RealmCategory
from version2 import RealmType
from version3 import SecurityFlag
from version2 import RealmFlag
from version5 import Realm
from version2 import TelemetryKey
from all import Version
from all import CMD_AUTH_LOGON_CHALLENGE_Client
from version3 import CMD_AUTH_LOGON_CHALLENGE_Server
from version3 import CMD_AUTH_LOGON_PROOF_Client
from version5 import CMD_AUTH_LOGON_PROOF_Server
from all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from version2 import CMD_AUTH_RECONNECT_CHALLENGE_Server
from version2 import CMD_AUTH_RECONNECT_PROOF_Client
from version5 import CMD_AUTH_RECONNECT_PROOF_Server
from version2 import CMD_REALM_LIST_Client


__all__ = [
    "Locale",
    "LoginResult",
    "Os",
    "Platform",
    "Population",
    "ProtocolVersion",
    "RealmCategory",
    "RealmType",
    "SecurityFlag",
    "RealmFlag",
    "Realm",
    "TelemetryKey",
    "Version",
    "CMD_AUTH_LOGON_CHALLENGE_Client",
    "CMD_AUTH_LOGON_CHALLENGE_Server",
    "CMD_AUTH_LOGON_PROOF_Client",
    "CMD_AUTH_LOGON_PROOF_Server",
    "CMD_AUTH_RECONNECT_CHALLENGE_Client",
    "CMD_AUTH_RECONNECT_CHALLENGE_Server",
    "CMD_AUTH_RECONNECT_PROOF_Client",
    "CMD_AUTH_RECONNECT_PROOF_Server",
    "CMD_REALM_LIST_Client",
    "CMD_REALM_LIST_Server",
    ]

@dataclasses.dataclass
class CMD_REALM_LIST_Server:
    realms: typing.List[Realm]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _size = int.from_bytes(await reader.readexactly(2), 'little')

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _header_padding = int.from_bytes(await reader.readexactly(4), 'little')

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        number_of_realms = int.from_bytes(await reader.readexactly(2), 'little')

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        realms = []
        for _ in range(0, number_of_realms):
            realms.append(await Realm.read(reader))

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _footer_padding = int.from_bytes(await reader.readexactly(2), 'little')

        return CMD_REALM_LIST_Server(
            realms,
            )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [16]

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(self._size())

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(0)

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(len(self.realms))

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            fmt, data = i.write(fmt, data)

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)

    def _size(self):
        size = 0

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            size += i._size()

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        return size - 2


