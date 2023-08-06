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
from .all import Os
from .all import Platform
from .all import ProtocolVersion
from .all import Version
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client


__all__ = [
    "Locale",
    "LoginResult",
    "Os",
    "Platform",
    "ProtocolVersion",
    "RealmCategory",
    "RealmType",
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
    "CMD_AUTH_RECONNECT_PROOF_Server",
    "CMD_AUTH_RECONNECT_PROOF_Client",
    "CMD_REALM_LIST_Server",
    "CMD_REALM_LIST_Client",
    ]

class LoginResult(enum.Enum):
    SUCCESS = 0
    FAIL_UNKNOWN0 = 1
    FAIL_UNKNOWN1 = 2
    FAIL_BANNED = 3
    FAIL_UNKNOWN_ACCOUNT = 4
    FAIL_INCORRECT_PASSWORD = 5
    FAIL_ALREADY_ONLINE = 6
    FAIL_NO_TIME = 7
    FAIL_DB_BUSY = 8
    FAIL_VERSION_INVALID = 9
    LOGIN_DOWNLOAD_FILE = 10
    FAIL_INVALID_SERVER = 11
    FAIL_SUSPENDED = 12
    FAIL_NO_ACCESS = 13
    SUCCESS_SURVEY = 14
    FAIL_PARENTALCONTROL = 15


class RealmCategory(enum.Enum):
    DEFAULT = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5


class RealmType(enum.Enum):
    PLAYER_VS_ENVIRONMENT = 0
    PLAYER_VS_PLAYER = 1
    ROLEPLAYING = 6
    ROLEPLAYING_PLAYER_VS_PLAYER = 8


class RealmFlag(enum.Flag):
    NONE = 0
    INVALID = 1
    OFFLINE = 2
    FORCE_BLUE_RECOMMENDED = 32
    FORCE_GREEN_RECOMMENDED = 64
    FORCE_RED_FULL = 128


@dataclasses.dataclass
class Realm:
    realm_type: RealmType
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
        realm_type = RealmType(await read_int(reader, 4))

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
            flag=flag,
            name=name,
            address=address,
            population=population,
            number_of_characters_on_realm=number_of_characters_on_realm,
            category=category,
            realm_id=realm_id,
        )

    def write(self, _fmt, _data):
        _fmt += f'IB{len(self.name)}sB{len(self.address)}sBfBBB'
        _data.extend([self.realm_type.value, self.flag.value, self.name.encode('utf-8'), 0, self.address.encode('utf-8'), 0, self.population, self.number_of_characters_on_realm, self.category.value, self.realm_id])
        return _fmt, _data

    def size(self) -> int:
        return 14 + len(self.name) + len(self.address)


@dataclasses.dataclass
class TelemetryKey:
    unknown1: int
    unknown2: int
    unknown3: typing.List[int]
    cd_key_proof: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # unknown1: u16
        unknown1 = await read_int(reader, 2)

        # unknown2: u32
        unknown2 = await read_int(reader, 4)

        # unknown3: u8[4]
        unknown3 = []
        for _ in range(0, 4):
            unknown3.append(await read_int(reader, 1))

        # cd_key_proof: u8[20]
        cd_key_proof = []
        for _ in range(0, 20):
            cd_key_proof.append(await read_int(reader, 1))

        return TelemetryKey(
            unknown1=unknown1,
            unknown2=unknown2,
            unknown3=unknown3,
            cd_key_proof=cd_key_proof,
        )

    def write(self, _fmt, _data):
        _fmt += f'HI{len(self.unknown3)}B{len(self.cd_key_proof)}B'
        _data.extend([self.unknown1, self.unknown2, *self.unknown3, *self.cd_key_proof])
        return _fmt, _data


@dataclasses.dataclass
class CMD_AUTH_LOGON_CHALLENGE_Server:
    result: LoginResult
    server_public_key: typing.Optional[typing.List[int]] = None
    generator: typing.Optional[typing.List[int]] = None
    large_safe_prime: typing.Optional[typing.List[int]] = None
    salt: typing.Optional[typing.List[int]] = None
    crc_salt: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_public_key = None
        generator_length = None
        generator = None
        large_safe_prime_length = None
        large_safe_prime = None
        salt = None
        crc_salt = None
        # protocol_version: u8
        _protocol_version = await read_int(reader, 1)

        # result: LoginResult
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # server_public_key: u8[32]
            server_public_key = []
            for _ in range(0, 32):
                server_public_key.append(await read_int(reader, 1))

            # generator_length: u8
            generator_length = await read_int(reader, 1)

            # generator: u8[generator_length]
            generator = []
            for _ in range(0, generator_length):
                generator.append(await read_int(reader, 1))

            # large_safe_prime_length: u8
            large_safe_prime_length = await read_int(reader, 1)

            # large_safe_prime: u8[large_safe_prime_length]
            large_safe_prime = []
            for _ in range(0, large_safe_prime_length):
                large_safe_prime.append(await read_int(reader, 1))

            # salt: u8[32]
            salt = []
            for _ in range(0, 32):
                salt.append(await read_int(reader, 1))

            # crc_salt: u8[16]
            crc_salt = []
            for _ in range(0, 16):
                crc_salt.append(await read_int(reader, 1))

        return CMD_AUTH_LOGON_CHALLENGE_Server(
            result=result,
            server_public_key=server_public_key,
            generator=generator,
            large_safe_prime=large_safe_prime,
            salt=salt,
            crc_salt=crc_salt,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [0]

        _fmt += 'BB'
        _data.extend([0, self.result.value])
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.server_public_key)}BB{len(self.generator)}BB{len(self.large_safe_prime)}B{len(self.salt)}B{len(self.crc_salt)}B'
            _data.extend([*self.server_public_key, len(self.generator), *self.generator, len(self.large_safe_prime), *self.large_safe_prime, *self.salt, *self.crc_salt])
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Client:
    client_public_key: typing.List[int]
    client_proof: typing.List[int]
    crc_hash: typing.List[int]
    telemetry_keys: typing.List[TelemetryKey]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # client_public_key: u8[32]
        client_public_key = []
        for _ in range(0, 32):
            client_public_key.append(await read_int(reader, 1))

        # client_proof: u8[20]
        client_proof = []
        for _ in range(0, 20):
            client_proof.append(await read_int(reader, 1))

        # crc_hash: u8[20]
        crc_hash = []
        for _ in range(0, 20):
            crc_hash.append(await read_int(reader, 1))

        # number_of_telemetry_keys: u8
        number_of_telemetry_keys = await read_int(reader, 1)

        # telemetry_keys: TelemetryKey[number_of_telemetry_keys]
        telemetry_keys = []
        for _ in range(0, number_of_telemetry_keys):
            telemetry_keys.append(await TelemetryKey.read(reader))

        return CMD_AUTH_LOGON_PROOF_Client(
            client_public_key=client_public_key,
            client_proof=client_proof,
            crc_hash=crc_hash,
            telemetry_keys=telemetry_keys,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [1]

        _fmt += f'{len(self.client_public_key)}B{len(self.client_proof)}B{len(self.crc_hash)}BB'
        _data.extend([*self.client_public_key, *self.client_proof, *self.crc_hash, len(self.telemetry_keys)])
        # telemetry_keys: TelemetryKey[number_of_telemetry_keys]
        for i in self.telemetry_keys:
            _fmt, _data = i.write(_fmt, _data)

        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Server:
    result: LoginResult
    server_proof: typing.Optional[typing.List[int]] = None
    hardware_survey_id: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_proof = None
        hardware_survey_id = None
        # result: LoginResult
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # server_proof: u8[20]
            server_proof = []
            for _ in range(0, 20):
                server_proof.append(await read_int(reader, 1))

            # hardware_survey_id: u32
            hardware_survey_id = await read_int(reader, 4)

        return CMD_AUTH_LOGON_PROOF_Server(
            result=result,
            server_proof=server_proof,
            hardware_survey_id=hardware_survey_id,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [1]

        _fmt += 'B'
        _data.append(self.result.value)
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.server_proof)}BI'
            _data.extend([*self.server_proof, self.hardware_survey_id])
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_CHALLENGE_Server:
    result: LoginResult
    challenge_data: typing.Optional[typing.List[int]] = None
    checksum_salt: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        challenge_data = None
        checksum_salt = None
        # result: LoginResult
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # challenge_data: u8[16]
            challenge_data = []
            for _ in range(0, 16):
                challenge_data.append(await read_int(reader, 1))

            # checksum_salt: u8[16]
            checksum_salt = []
            for _ in range(0, 16):
                checksum_salt.append(await read_int(reader, 1))

        return CMD_AUTH_RECONNECT_CHALLENGE_Server(
            result=result,
            challenge_data=challenge_data,
            checksum_salt=checksum_salt,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [2]

        _fmt += 'B'
        _data.append(self.result.value)
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.challenge_data)}B{len(self.checksum_salt)}B'
            _data.extend([*self.challenge_data, *self.checksum_salt])
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

        return CMD_AUTH_RECONNECT_PROOF_Server(
            result=result,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [3]

        _fmt += 'B'
        _data.append(self.result.value)
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_PROOF_Client:
    proof_data: typing.List[int]
    client_proof: typing.List[int]
    client_checksum: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # proof_data: u8[16]
        proof_data = []
        for _ in range(0, 16):
            proof_data.append(await read_int(reader, 1))

        # client_proof: u8[20]
        client_proof = []
        for _ in range(0, 20):
            client_proof.append(await read_int(reader, 1))

        # client_checksum: u8[20]
        client_checksum = []
        for _ in range(0, 20):
            client_checksum.append(await read_int(reader, 1))

        # key_count: u8
        _key_count = await read_int(reader, 1)

        return CMD_AUTH_RECONNECT_PROOF_Client(
            proof_data=proof_data,
            client_proof=client_proof,
            client_checksum=client_checksum,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [3]

        _fmt += f'{len(self.proof_data)}B{len(self.client_proof)}B{len(self.client_checksum)}BB'
        _data.extend([*self.proof_data, *self.client_proof, *self.client_checksum, 0])
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


@dataclasses.dataclass
class CMD_REALM_LIST_Client:

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # padding: u32
        _padding = await read_int(reader, 4)

        return CMD_REALM_LIST_Client(
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [16]

        _fmt += 'I'
        _data.append(0)
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


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

