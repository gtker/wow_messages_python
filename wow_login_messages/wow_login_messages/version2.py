import asyncio
import dataclasses
import enum
import struct
import typing

from all import Locale
from all import Os
from all import Platform
from all import ProtocolVersion
from all import Version
from all import CMD_AUTH_LOGON_CHALLENGE_Client
from all import CMD_AUTH_RECONNECT_CHALLENGE_Client


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
        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='RealmType', upcast=True))
        realm_type = RealmType(int.from_bytes(await reader.readexactly(4), 'little'))

        # flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmFlag', upcast=False))
        flag = RealmFlag(int.from_bytes(await reader.readexactly(1), 'little'))

        # name: DataTypeCstring(data_type_tag='CString')
        name = (await reader.readuntil(b'\x00')).decode('utf-8').rstrip('\x00')

        # address: DataTypeCstring(data_type_tag='CString')
        address = (await reader.readuntil(b'\x00')).decode('utf-8').rstrip('\x00')

        # population: DataTypePopulation(data_type_tag='Population')
        population = float.from_bytes(await reader.readexactly(4), 'little')

        # number_of_characters_on_realm: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_characters_on_realm = int.from_bytes(await reader.readexactly(1), 'little')

        # category: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmCategory', upcast=False))
        category = RealmCategory(int.from_bytes(await reader.readexactly(1), 'little'))

        # realm_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        realm_id = int.from_bytes(await reader.readexactly(1), 'little')

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

    def write(self, fmt, data):
        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='RealmType', upcast=True))
        fmt += 'I'
        data.append(self.realm_type.value)

        # flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmFlag', upcast=False))
        fmt += 'B'
        data.append(self.flag.value)

        # name: DataTypeCstring(data_type_tag='CString')
        fmt += f'{len(self.name)}sB'
        data.append(self.name.encode('utf-8'))
        data.append(0)

        # address: DataTypeCstring(data_type_tag='CString')
        fmt += f'{len(self.address)}sB'
        data.append(self.address.encode('utf-8'))
        data.append(0)

        # population: DataTypePopulation(data_type_tag='Population')
        fmt += 'f'
        data.append(self.population)

        # number_of_characters_on_realm: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.number_of_characters_on_realm)

        # category: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmCategory', upcast=False))
        fmt += 'B'
        data.append(self.category.value)

        # realm_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.realm_id)

        return fmt, data

    def _size(self) -> int:
        size = 0

        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='RealmType', upcast=True))
        size += 4

        # flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmFlag', upcast=False))
        size += 1

        # name: DataTypeCstring(data_type_tag='CString')
        size += len(self.name) + 1

        # address: DataTypeCstring(data_type_tag='CString')
        size += len(self.address) + 1

        # population: DataTypePopulation(data_type_tag='Population')
        size += 4

        # number_of_characters_on_realm: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # category: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmCategory', upcast=False))
        size += 1

        # realm_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        return size


@dataclasses.dataclass
class TelemetryKey:
    unknown1: int
    unknown2: int
    unknown3: typing.List[int]
    cd_key_proof: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # unknown1: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        unknown1 = int.from_bytes(await reader.readexactly(2), 'little')

        # unknown2: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        unknown2 = int.from_bytes(await reader.readexactly(4), 'little')

        # unknown3: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='4')))
        unknown3 = []
        for _ in range(0, 4):
            unknown3.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # cd_key_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        cd_key_proof = []
        for _ in range(0, 20):
            cd_key_proof.append(int.from_bytes(await reader.readexactly(1), 'little'))

        return TelemetryKey(
            unknown1=unknown1,
            unknown2=unknown2,
            unknown3=unknown3,
            cd_key_proof=cd_key_proof,
        )

    def write(self, fmt, data):
        # unknown1: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(self.unknown1)

        # unknown2: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(self.unknown2)

        # unknown3: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='4')))
        fmt += f'{len(self.unknown3)}B'
        data.extend(self.unknown3)

        # cd_key_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        fmt += f'{len(self.cd_key_proof)}B'
        data.extend(self.cd_key_proof)

        return fmt, data


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
        # protocol_version: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        _protocol_version = int.from_bytes(await reader.readexactly(1), 'little')

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        if result == LoginResult.SUCCESS:
            # server_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            server_public_key = []
            for _ in range(0, 32):
                server_public_key.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # generator_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            generator_length = int.from_bytes(await reader.readexactly(1), 'little')

            # generator: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='generator_length')))
            generator = []
            for _ in range(0, generator_length):
                generator.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # large_safe_prime_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            large_safe_prime_length = int.from_bytes(await reader.readexactly(1), 'little')

            # large_safe_prime: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='large_safe_prime_length')))
            large_safe_prime = []
            for _ in range(0, large_safe_prime_length):
                large_safe_prime.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            salt = []
            for _ in range(0, 32):
                salt.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # crc_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            crc_salt = []
            for _ in range(0, 16):
                crc_salt.append(int.from_bytes(await reader.readexactly(1), 'little'))

        return CMD_AUTH_LOGON_CHALLENGE_Server(
            result=result,
            server_public_key=server_public_key,
            generator=generator,
            large_safe_prime=large_safe_prime,
            salt=salt,
            crc_salt=crc_salt,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [0]

        # protocol_version: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(0)

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        if self.result == LoginResult.SUCCESS:
            # server_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            fmt += f'{len(self.server_public_key)}B'
            data.extend(self.server_public_key)

            # generator_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            fmt += 'B'
            data.append(len(self.generator))

            # generator: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='generator_length')))
            fmt += f'{len(self.generator)}B'
            data.extend(self.generator)

            # large_safe_prime_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            fmt += 'B'
            data.append(len(self.large_safe_prime))

            # large_safe_prime: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='large_safe_prime_length')))
            fmt += f'{len(self.large_safe_prime)}B'
            data.extend(self.large_safe_prime)

            # salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            fmt += f'{len(self.salt)}B'
            data.extend(self.salt)

            # crc_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            fmt += f'{len(self.crc_salt)}B'
            data.extend(self.crc_salt)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Client:
    client_public_key: typing.List[int]
    client_proof: typing.List[int]
    crc_hash: typing.List[int]
    telemetry_keys: typing.List[TelemetryKey]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # client_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
        client_public_key = []
        for _ in range(0, 32):
            client_public_key.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # client_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        client_proof = []
        for _ in range(0, 20):
            client_proof.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # crc_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        crc_hash = []
        for _ in range(0, 20):
            crc_hash.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # number_of_telemetry_keys: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_telemetry_keys = int.from_bytes(await reader.readexactly(1), 'little')

        # telemetry_keys: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=30, minimum_size=30), type_name='TelemetryKey')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_telemetry_keys')))
        telemetry_keys = []
        for _ in range(0, number_of_telemetry_keys):
            telemetry_keys.append(await TelemetryKey.read(reader))

        return CMD_AUTH_LOGON_PROOF_Client(
            client_public_key=client_public_key,
            client_proof=client_proof,
            crc_hash=crc_hash,
            telemetry_keys=telemetry_keys,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [1]

        # client_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
        fmt += f'{len(self.client_public_key)}B'
        data.extend(self.client_public_key)

        # client_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        fmt += f'{len(self.client_proof)}B'
        data.extend(self.client_proof)

        # crc_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        fmt += f'{len(self.crc_hash)}B'
        data.extend(self.crc_hash)

        # number_of_telemetry_keys: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(len(self.telemetry_keys))

        # telemetry_keys: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=30, minimum_size=30), type_name='TelemetryKey')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_telemetry_keys')))
        for i in self.telemetry_keys:
            fmt, data = i.write(fmt, data)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Server:
    result: LoginResult
    server_proof: typing.Optional[typing.List[int]] = None
    hardware_survey_id: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_proof = None
        hardware_survey_id = None
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        if result == LoginResult.SUCCESS:
            # server_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            server_proof = []
            for _ in range(0, 20):
                server_proof.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            hardware_survey_id = int.from_bytes(await reader.readexactly(4), 'little')

        return CMD_AUTH_LOGON_PROOF_Server(
            result=result,
            server_proof=server_proof,
            hardware_survey_id=hardware_survey_id,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [1]

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        if self.result == LoginResult.SUCCESS:
            # server_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            fmt += f'{len(self.server_proof)}B'
            data.extend(self.server_proof)

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            fmt += 'I'
            data.append(self.hardware_survey_id)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_CHALLENGE_Server:
    result: LoginResult
    challenge_data: typing.Optional[typing.List[int]] = None
    checksum_salt: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        challenge_data = None
        checksum_salt = None
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        if result == LoginResult.SUCCESS:
            # challenge_data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            challenge_data = []
            for _ in range(0, 16):
                challenge_data.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # checksum_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            checksum_salt = []
            for _ in range(0, 16):
                checksum_salt.append(int.from_bytes(await reader.readexactly(1), 'little'))

        return CMD_AUTH_RECONNECT_CHALLENGE_Server(
            result=result,
            challenge_data=challenge_data,
            checksum_salt=checksum_salt,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [2]

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        if self.result == LoginResult.SUCCESS:
            # challenge_data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            fmt += f'{len(self.challenge_data)}B'
            data.extend(self.challenge_data)

            # checksum_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            fmt += f'{len(self.checksum_salt)}B'
            data.extend(self.checksum_salt)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_PROOF_Client:
    proof_data: typing.List[int]
    client_proof: typing.List[int]
    client_checksum: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # proof_data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
        proof_data = []
        for _ in range(0, 16):
            proof_data.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # client_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        client_proof = []
        for _ in range(0, 20):
            client_proof.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # client_checksum: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        client_checksum = []
        for _ in range(0, 20):
            client_checksum.append(int.from_bytes(await reader.readexactly(1), 'little'))

        # key_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        _key_count = int.from_bytes(await reader.readexactly(1), 'little')

        return CMD_AUTH_RECONNECT_PROOF_Client(
            proof_data=proof_data,
            client_proof=client_proof,
            client_checksum=client_checksum,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [3]

        # proof_data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
        fmt += f'{len(self.proof_data)}B'
        data.extend(self.proof_data)

        # client_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        fmt += f'{len(self.client_proof)}B'
        data.extend(self.client_proof)

        # client_checksum: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        fmt += f'{len(self.client_checksum)}B'
        data.extend(self.client_checksum)

        # key_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_PROOF_Server:
    result: LoginResult

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        return CMD_AUTH_RECONNECT_PROOF_Server(
            result=result,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [3]

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_REALM_LIST_Client:

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _padding = int.from_bytes(await reader.readexactly(4), 'little')

        return CMD_REALM_LIST_Client(
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [16]

        # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_REALM_LIST_Server:
    realms: typing.List[Realm]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _size = int.from_bytes(await reader.readexactly(2), 'little')

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _header_padding = int.from_bytes(await reader.readexactly(4), 'little')

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_realms = int.from_bytes(await reader.readexactly(1), 'little')

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=524, minimum_size=14), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        realms = []
        for _ in range(0, number_of_realms):
            realms.append(await Realm.read(reader))

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _footer_padding = int.from_bytes(await reader.readexactly(2), 'little')

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

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(len(self.realms))

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=524, minimum_size=14), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
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

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=524, minimum_size=14), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            size += i._size()

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        return size - 2


