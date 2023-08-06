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
from .all import Version
from .version2 import TelemetryKey
from .version3 import CMD_AUTH_LOGON_CHALLENGE_Server
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .version3 import CMD_AUTH_LOGON_PROOF_Client
from .version2 import CMD_AUTH_RECONNECT_CHALLENGE_Server
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from .version2 import CMD_AUTH_RECONNECT_PROOF_Client
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
class Realm:
    realm_type: RealmType
    locked: bool
    flag: RealmFlag
    name: str
    address: str
    population: float
    number_of_characters_on_realm: int
    category: RealmCategory
    realm_id: int

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # realm_type: RealmType
        realm_type = RealmType(await read_int(reader, 1))

        # locked: Bool8
        locked = await read_bool(reader, 1)

        # flag: RealmFlag
        flag = RealmFlag(await read_int(reader, 1))

        # name: CString
        name = await read_cstring(reader)

        # address: CString
        address = await read_cstring(reader)

        # population: Population
        population = await read_float(reader)

        # number_of_characters_on_realm: u8
        number_of_characters_on_realm = await read_int(reader, 1)

        # category: RealmCategory
        category = RealmCategory(await read_int(reader, 1))

        # realm_id: u8
        realm_id = await read_int(reader, 1)

        return Realm(
            realm_type=realm_type,
            locked=locked,
            flag=flag,
            name=name,
            address=address,
            population=population,
            number_of_characters_on_realm=number_of_characters_on_realm,
            category=category,
            realm_id=realm_id,
        )

    def write(self, _fmt, _data):
        _fmt += f'BBB{len(self.name)}sB{len(self.address)}sBfBBB'
        _data.extend([self.realm_type.value, self.locked, self.flag.value, self.name.encode('utf-8'), 0, self.address.encode('utf-8'), 0, self.population, self.number_of_characters_on_realm, self.category.value, self.realm_id])
        return _fmt, _data

    def size(self) -> int:
        return 12 + len(self.name) + len(self.address)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Server:
    result: LoginResult
    server_proof: typing.Optional[typing.List[int]] = None
    hardware_survey_id: typing.Optional[int] = None
    unknown: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_proof = None
        hardware_survey_id = None
        unknown = None
        # result: LoginResult
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # server_proof: u8[20]
            server_proof = []
            for _ in range(0, 20):
                server_proof.append(await read_int(reader, 1))

            # hardware_survey_id: u32
            hardware_survey_id = await read_int(reader, 4)

            # unknown: u16
            unknown = await read_int(reader, 2)

        return CMD_AUTH_LOGON_PROOF_Server(
            result=result,
            server_proof=server_proof,
            hardware_survey_id=hardware_survey_id,
            unknown=unknown,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [1]

        _fmt += 'B'
        _data.append(self.result.value)
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.server_proof)}BIH'
            _data.extend([*self.server_proof, self.hardware_survey_id, self.unknown])
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_PROOF_Server:
    result: LoginResult

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # result: LoginResult
        result = LoginResult(await read_int(reader, 1))

        # padding: u16
        _padding = await read_int(reader, 2)

        return CMD_AUTH_RECONNECT_PROOF_Server(
            result=result,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [3]

        _fmt += 'BH'
        _data.extend([self.result.value, 0])
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_REALM_LIST_Server:
    realms: typing.List[Realm]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # size: u16
        _size = await read_int(reader, 2)

        # header_padding: u32
        _header_padding = await read_int(reader, 4)

        # number_of_realms: u8
        number_of_realms = await read_int(reader, 1)

        # realms: Realm[number_of_realms]
        realms = []
        for _ in range(0, number_of_realms):
            realms.append(await Realm.read(reader))

        # footer_padding: u16
        _footer_padding = await read_int(reader, 2)

        return CMD_REALM_LIST_Server(
            realms=realms,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [16]

        _fmt += 'HIB'
        _data.extend([self.size(), 0, len(self.realms)])
        # realms: Realm[number_of_realms]
        for i in self.realms:
            _fmt, _data = i.write(_fmt, _data)

        # footer_padding: u16
        _fmt += 'H'
        _data.append(0)

        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)

    def size(self) -> int:
        return 7 + sum([i.size() for i in self.realms])


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

