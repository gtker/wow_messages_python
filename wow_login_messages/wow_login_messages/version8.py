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
from .all import Os
from .all import Platform
from .all import ProtocolVersion
from .version2 import RealmCategory
from .version2 import RealmType
from .all import Version
from .version2 import TelemetryKey
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
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
    "AccountFlag",
    "RealmFlag",
    "SecurityFlag",
    "Version",
    "Realm",
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
    FAIL_LOCKED_ENFORCED = 16


class AccountFlag(enum.Flag):
    GM = 1
    TRIAL = 8
    PROPASS = 8388608


class RealmFlag(enum.Flag):
    NONE = 0
    INVALID = 1
    OFFLINE = 2
    SPECIFY_BUILD = 4
    FORCE_BLUE_RECOMMENDED = 32
    FORCE_GREEN_RECOMMENDED = 64
    FORCE_RED_FULL = 128


class SecurityFlag(enum.Flag):
    NONE = 0
    PIN = 1
    MATRIX_CARD = 2
    AUTHENTICATOR = 4


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
    version: typing.Optional[Version] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        version = None
        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmType', upcast=False))
        realm_type = RealmType(await read_int(reader, 1))

        # locked: DataTypeBool(data_type_tag='Bool', content=<IntegerType.U8: 'U8'>)
        locked = await read_bool(reader, 1)

        # flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmFlag', upcast=False))
        flag = RealmFlag(await read_int(reader, 1))

        # name: DataTypeCstring(data_type_tag='CString')
        name = await read_cstring(reader)

        # address: DataTypeCstring(data_type_tag='CString')
        address = await read_cstring(reader)

        # population: DataTypePopulation(data_type_tag='Population')
        population = await read_float(reader)

        # number_of_characters_on_realm: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_characters_on_realm = await read_int(reader, 1)

        # category: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmCategory', upcast=False))
        category = RealmCategory(await read_int(reader, 1))

        # realm_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        realm_id = await read_int(reader, 1)

        if RealmFlag.SPECIFY_BUILD in flag:
            # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
            version = await Version.read(reader)

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
            version=version,
        )

    def write(self, fmt, data):
        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmType', upcast=False))
        fmt += 'B'
        data.append(self.realm_type.value)

        # locked: DataTypeBool(data_type_tag='Bool', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.locked)

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

        if RealmFlag.SPECIFY_BUILD in self.flag:
            # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
            fmt, data = self.version.write(fmt, data)

        return fmt, data

    def _size(self) -> int:
        size = 0

        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmType', upcast=False))
        size += 1

        # locked: DataTypeBool(data_type_tag='Bool', content=<IntegerType.U8: 'U8'>)
        size += 1

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

        if RealmFlag.SPECIFY_BUILD in self.flag:
            # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
            size += 5


        return size


@dataclasses.dataclass
class CMD_AUTH_LOGON_CHALLENGE_Server:
    result: LoginResult
    server_public_key: typing.Optional[typing.List[int]] = None
    generator: typing.Optional[typing.List[int]] = None
    large_safe_prime: typing.Optional[typing.List[int]] = None
    salt: typing.Optional[typing.List[int]] = None
    crc_salt: typing.Optional[typing.List[int]] = None
    security_flag: typing.Optional[SecurityFlag] = None
    pin_grid_seed: typing.Optional[int] = None
    pin_salt: typing.Optional[typing.List[int]] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    digit_count: typing.Optional[int] = None
    challenge_count: typing.Optional[int] = None
    seed: typing.Optional[int] = None
    required: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_public_key = None
        generator_length = None
        generator = None
        large_safe_prime_length = None
        large_safe_prime = None
        salt = None
        crc_salt = None
        security_flag = None
        pin_grid_seed = None
        pin_salt = None
        width = None
        height = None
        digit_count = None
        challenge_count = None
        seed = None
        required = None
        # protocol_version: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        _protocol_version = await read_int(reader, 1)

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # server_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            server_public_key = []
            for _ in range(0, 32):
                server_public_key.append(await read_int(reader, 1))

            # generator_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            generator_length = await read_int(reader, 1)

            # generator: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='generator_length')))
            generator = []
            for _ in range(0, generator_length):
                generator.append(await read_int(reader, 1))

            # large_safe_prime_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            large_safe_prime_length = await read_int(reader, 1)

            # large_safe_prime: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='large_safe_prime_length')))
            large_safe_prime = []
            for _ in range(0, large_safe_prime_length):
                large_safe_prime.append(await read_int(reader, 1))

            # salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
            salt = []
            for _ in range(0, 32):
                salt.append(await read_int(reader, 1))

            # crc_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            crc_salt = []
            for _ in range(0, 16):
                crc_salt.append(await read_int(reader, 1))

            # security_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
            security_flag = SecurityFlag(await read_int(reader, 1))

            if SecurityFlag.PIN in security_flag:
                # pin_grid_seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
                pin_grid_seed = await read_int(reader, 4)

                # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
                pin_salt = []
                for _ in range(0, 16):
                    pin_salt.append(await read_int(reader, 1))

            if SecurityFlag.MATRIX_CARD in security_flag:
                # width: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                width = await read_int(reader, 1)

                # height: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                height = await read_int(reader, 1)

                # digit_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                digit_count = await read_int(reader, 1)

                # challenge_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                challenge_count = await read_int(reader, 1)

                # seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U64: 'U64'>)
                seed = await read_int(reader, 8)

            if SecurityFlag.AUTHENTICATOR in security_flag:
                # required: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                required = await read_int(reader, 1)

        return CMD_AUTH_LOGON_CHALLENGE_Server(
            result=result,
            server_public_key=server_public_key,
            generator=generator,
            large_safe_prime=large_safe_prime,
            salt=salt,
            crc_salt=crc_salt,
            security_flag=security_flag,
            pin_grid_seed=pin_grid_seed,
            pin_salt=pin_salt,
            width=width,
            height=height,
            digit_count=digit_count,
            challenge_count=challenge_count,
            seed=seed,
            required=required,
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

            # security_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
            fmt += 'B'
            data.append(self.security_flag.value)

            if SecurityFlag.PIN in self.security_flag:
                # pin_grid_seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
                fmt += 'I'
                data.append(self.pin_grid_seed)

                # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
                fmt += f'{len(self.pin_salt)}B'
                data.extend(self.pin_salt)

            if SecurityFlag.MATRIX_CARD in self.security_flag:
                # width: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                fmt += 'B'
                data.append(self.width)

                # height: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                fmt += 'B'
                data.append(self.height)

                # digit_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                fmt += 'B'
                data.append(self.digit_count)

                # challenge_count: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                fmt += 'B'
                data.append(self.challenge_count)

                # seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U64: 'U64'>)
                fmt += 'Q'
                data.append(self.seed)

            if SecurityFlag.AUTHENTICATOR in self.security_flag:
                # required: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
                fmt += 'B'
                data.append(self.required)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Client:
    client_public_key: typing.List[int]
    client_proof: typing.List[int]
    crc_hash: typing.List[int]
    telemetry_keys: typing.List[TelemetryKey]
    security_flag: SecurityFlag
    pin_salt: typing.Optional[typing.List[int]] = None
    pin_hash: typing.Optional[typing.List[int]] = None
    matrix_card_proof: typing.Optional[typing.List[int]] = None
    tokens: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        pin_salt = None
        pin_hash = None
        matrix_card_proof = None
        amount_of_tokens = None
        tokens = None
        # client_public_key: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='32')))
        client_public_key = []
        for _ in range(0, 32):
            client_public_key.append(await read_int(reader, 1))

        # client_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        client_proof = []
        for _ in range(0, 20):
            client_proof.append(await read_int(reader, 1))

        # crc_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
        crc_hash = []
        for _ in range(0, 20):
            crc_hash.append(await read_int(reader, 1))

        # number_of_telemetry_keys: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_telemetry_keys = await read_int(reader, 1)

        # telemetry_keys: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=30, minimum_size=30), type_name='TelemetryKey')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_telemetry_keys')))
        telemetry_keys = []
        for _ in range(0, number_of_telemetry_keys):
            telemetry_keys.append(await TelemetryKey.read(reader))

        # security_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
        security_flag = SecurityFlag(await read_int(reader, 1))

        if SecurityFlag.PIN in security_flag:
            # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            pin_salt = []
            for _ in range(0, 16):
                pin_salt.append(await read_int(reader, 1))

            # pin_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            pin_hash = []
            for _ in range(0, 20):
                pin_hash.append(await read_int(reader, 1))

        if SecurityFlag.MATRIX_CARD in security_flag:
            # matrix_card_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            matrix_card_proof = []
            for _ in range(0, 20):
                matrix_card_proof.append(await read_int(reader, 1))

        if SecurityFlag.AUTHENTICATOR in security_flag:
            # amount_of_tokens: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            amount_of_tokens = await read_int(reader, 1)

            # tokens: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='amount_of_tokens')))
            tokens = []
            for _ in range(0, amount_of_tokens):
                tokens.append(await read_int(reader, 1))

        return CMD_AUTH_LOGON_PROOF_Client(
            client_public_key=client_public_key,
            client_proof=client_proof,
            crc_hash=crc_hash,
            telemetry_keys=telemetry_keys,
            security_flag=security_flag,
            pin_salt=pin_salt,
            pin_hash=pin_hash,
            matrix_card_proof=matrix_card_proof,
            tokens=tokens,
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

        # security_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
        fmt += 'B'
        data.append(self.security_flag.value)

        if SecurityFlag.PIN in self.security_flag:
            # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            fmt += f'{len(self.pin_salt)}B'
            data.extend(self.pin_salt)

            # pin_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            fmt += f'{len(self.pin_hash)}B'
            data.extend(self.pin_hash)

        if SecurityFlag.MATRIX_CARD in self.security_flag:
            # matrix_card_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            fmt += f'{len(self.matrix_card_proof)}B'
            data.extend(self.matrix_card_proof)

        if SecurityFlag.AUTHENTICATOR in self.security_flag:
            # amount_of_tokens: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
            fmt += 'B'
            data.append(len(self.tokens))

            # tokens: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='amount_of_tokens')))
            fmt += f'{len(self.tokens)}B'
            data.extend(self.tokens)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Server:
    result: LoginResult
    server_proof: typing.Optional[typing.List[int]] = None
    account_flag: typing.Optional[AccountFlag] = None
    hardware_survey_id: typing.Optional[int] = None
    unknown_flags: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_proof = None
        account_flag = None
        hardware_survey_id = None
        unknown_flags = None
        padding = None
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # server_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            server_proof = []
            for _ in range(0, 20):
                server_proof.append(await read_int(reader, 1))

            # account_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U32: 'U32'>, type_name='AccountFlag', upcast=False))
            account_flag = AccountFlag(await read_int(reader, 4))

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            hardware_survey_id = await read_int(reader, 4)

            # unknown_flags: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            unknown_flags = await read_int(reader, 2)

        else:
            # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            _padding = await read_int(reader, 2)

        return CMD_AUTH_LOGON_PROOF_Server(
            result=result,
            server_proof=server_proof,
            account_flag=account_flag,
            hardware_survey_id=hardware_survey_id,
            unknown_flags=unknown_flags,
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

            # account_flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U32: 'U32'>, type_name='AccountFlag', upcast=False))
            fmt += 'I'
            data.append(self.account_flag.value)

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            fmt += 'I'
            data.append(self.hardware_survey_id)

            # unknown_flags: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            fmt += 'H'
            data.append(self.unknown_flags)

        else:
            # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            fmt += 'H'
            data.append(0)

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
        result = LoginResult(await read_int(reader, 1))

        if result == LoginResult.SUCCESS:
            # challenge_data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            challenge_data = []
            for _ in range(0, 16):
                challenge_data.append(await read_int(reader, 1))

            # checksum_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            checksum_salt = []
            for _ in range(0, 16):
                checksum_salt.append(await read_int(reader, 1))

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
class CMD_AUTH_RECONNECT_PROOF_Server:
    result: LoginResult

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(await read_int(reader, 1))

        # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _padding = await read_int(reader, 2)

        return CMD_AUTH_RECONNECT_PROOF_Server(
            result=result,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [3]

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)


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

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=527, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
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

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=527, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
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

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', content=ArrayTypeStructContent(sizes=Sizes(constant_sized=False, maximum_size=527, minimum_size=12), type_name='Realm')), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
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


