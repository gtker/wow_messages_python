import asyncio
import dataclasses
import enum
import struct
import typing
import zlib
from .util import read_string
from .util import read_bool
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
from .version6 import CMD_REALM_LIST_Server


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

ClientOpcode = typing.Union[
    CMD_AUTH_LOGON_CHALLENGE_Client,
    CMD_AUTH_LOGON_PROOF_Client,
    CMD_AUTH_RECONNECT_CHALLENGE_Client,
    CMD_AUTH_RECONNECT_PROOF_Client,
    CMD_REALM_LIST_Client,
    ]


async def read_client_opcode(reader: asyncio.StreamReader) -> typing.Optional[ClientOpcode]:
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


async def expect_client_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ClientOpcode]) -> typing.Optional[ClientOpcode]:
    o = await read_client_opcode(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None


ServerOpcode = typing.Union[
    CMD_AUTH_LOGON_CHALLENGE_Server,
    CMD_AUTH_LOGON_PROOF_Server,
    CMD_AUTH_RECONNECT_CHALLENGE_Server,
    CMD_AUTH_RECONNECT_PROOF_Server,
    CMD_REALM_LIST_Server,
    ]


async def read_server_opcode(reader: asyncio.StreamReader) -> typing.Optional[ServerOpcode]:
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
        return None


async def expect_server_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ServerOpcode]) -> typing.Optional[ServerOpcode]:
    o = await read_server_opcode(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None

