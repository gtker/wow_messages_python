import asyncio
import dataclasses
import enum
import struct
import typing
from .util import read_string
from .util import read_int
from .util import read_cstring
from .util import read_float

from .all import Locale
from .version2 import LoginResult
from .all import Os
from .all import Platform
from .all import ProtocolVersion
from .version2 import RealmCategory
from .version2 import RealmType
from .version3 import SecurityFlag
from .version2 import RealmFlag
from .version5 import Realm
from .all import Version
from .version2 import TelemetryKey
from .version3 import CMD_AUTH_LOGON_CHALLENGE_Server
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .version3 import CMD_AUTH_LOGON_PROOF_Client
from .version5 import CMD_AUTH_LOGON_PROOF_Server
from .version2 import CMD_AUTH_RECONNECT_CHALLENGE_Server
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from .version2 import CMD_AUTH_RECONNECT_PROOF_Client
from .version5 import CMD_AUTH_RECONNECT_PROOF_Server
from .version2 import CMD_REALM_LIST_Client


__all__ = [
    "Locale",
    "LoginResult",
    "Os",
    "Platform",
    "ProtocolVersion",
    "RealmCategory",
    "RealmType",
    "SecurityFlag",
    "RealmFlag",
    "Realm",
    "Version",
    "TelemetryKey",
    "CMD_AUTH_LOGON_CHALLENGE_Server",
    "CMD_AUTH_LOGON_CHALLENGE_Client",
    "CMD_AUTH_LOGON_PROOF_Client",
    "CMD_AUTH_LOGON_PROOF_Server",
    "CMD_AUTH_RECONNECT_CHALLENGE_Server",
    "CMD_AUTH_RECONNECT_CHALLENGE_Client",
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
        _size = await read_int(reader, 2)

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _header_padding = await read_int(reader, 4)

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        number_of_realms = await read_int(reader, 2)

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=522, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        realms = []
        for _ in range(0, number_of_realms):
            realms.append(await Realm.read(reader))

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _footer_padding = await read_int(reader, 2)

        return CMD_REALM_LIST_Server(
            realms=realms,
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

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=522, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            fmt, data = i.write(fmt, data)

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)

    def _size(self) -> int:
        size = 0

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=522, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            size += i._size()

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        return size - 2


async def read_opcode_server(reader: asyncio.StreamReader):
    opcode = int.from_bytes(await reader.readexactly(1), 'little')
    if opcode == 0x00:
        return await CMD_AUTH_LOGON_CHALLENGE_Client.read(reader)
    if opcode == 0x01:
        return await CMD_AUTH_LOGON_PROOF_Client.read(reader)
    if opcode == 0x02:
        return await CMD_AUTH_RECONNECT_CHALLENGE_Client.read(reader)
    if opcode == 0x03:
        return await CMD_AUTH_RECONNECT_PROOF_Client.read(reader)
    if opcode == 0x10:
        return await CMD_REALM_LIST_Client.read(reader)
    else:
        raise Exception(f'incorrect opcode {opcode}')


async def read_opcode_client(reader: asyncio.StreamReader):
    opcode = int.from_bytes(await reader.readexactly(1), 'little')
    if opcode == 0x00:
        return await CMD_AUTH_LOGON_CHALLENGE_Server.read(reader)
    if opcode == 0x01:
        return await CMD_AUTH_LOGON_PROOF_Server.read(reader)
    if opcode == 0x02:
        return await CMD_AUTH_RECONNECT_CHALLENGE_Server.read(reader)
    if opcode == 0x03:
        return await CMD_AUTH_RECONNECT_PROOF_Server.read(reader)
    if opcode == 0x10:
        return await CMD_REALM_LIST_Server.read(reader)
    else:
        raise Exception(f'incorrect opcode {opcode}')


