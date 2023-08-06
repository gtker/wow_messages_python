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
from .version2 import RealmFlag
from .version2 import Realm
from .all import Version
from .version2 import TelemetryKey
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .version2 import CMD_AUTH_LOGON_PROOF_Server
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from .version2 import CMD_REALM_LIST_Server
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
    "CMD_AUTH_LOGON_PROOF_Server",
    "CMD_AUTH_LOGON_PROOF_Client",
    "CMD_AUTH_RECONNECT_CHALLENGE_Client",
    "CMD_SURVEY_RESULT",
    "CMD_REALM_LIST_Server",
    "CMD_REALM_LIST_Client",
    "CMD_XFER_INITIATE",
    "CMD_XFER_DATA",
    "CMD_XFER_ACCEPT",
    "CMD_XFER_RESUME",
    "CMD_XFER_CANCEL",
    ]

class SecurityFlag(enum.Enum):
    NONE = 0
    PIN = 1


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

            # security_flag: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
            security_flag = SecurityFlag(await read_int(reader, 1))

            if security_flag == SecurityFlag.PIN:
                # pin_grid_seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
                pin_grid_seed = await read_int(reader, 4)

                # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
                pin_salt = []
                for _ in range(0, 16):
                    pin_salt.append(await read_int(reader, 1))

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

            # security_flag: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
            fmt += 'B'
            data.append(self.security_flag.value)

            if self.security_flag == SecurityFlag.PIN:
                # pin_grid_seed: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
                fmt += 'I'
                data.append(self.pin_grid_seed)

                # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
                fmt += f'{len(self.pin_salt)}B'
                data.extend(self.pin_salt)

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

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        pin_salt = None
        pin_hash = None
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

        # security_flag: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
        security_flag = SecurityFlag(await read_int(reader, 1))

        if security_flag == SecurityFlag.PIN:
            # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            pin_salt = []
            for _ in range(0, 16):
                pin_salt.append(await read_int(reader, 1))

            # pin_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            pin_hash = []
            for _ in range(0, 20):
                pin_hash.append(await read_int(reader, 1))

        return CMD_AUTH_LOGON_PROOF_Client(
            client_public_key=client_public_key,
            client_proof=client_proof,
            crc_hash=crc_hash,
            telemetry_keys=telemetry_keys,
            security_flag=security_flag,
            pin_salt=pin_salt,
            pin_hash=pin_hash,
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

        # security_flag: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='SecurityFlag', upcast=False))
        fmt += 'B'
        data.append(self.security_flag.value)

        if self.security_flag == SecurityFlag.PIN:
            # pin_salt: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='16')))
            fmt += f'{len(self.pin_salt)}B'
            data.extend(self.pin_salt)

            # pin_hash: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            fmt += f'{len(self.pin_hash)}B'
            data.extend(self.pin_hash)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_SURVEY_RESULT:
    survey_id: int
    error: int
    data: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        survey_id = await read_int(reader, 4)

        # error: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        error = await read_int(reader, 1)

        # compressed_data_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        compressed_data_length = await read_int(reader, 2)

        # data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='compressed_data_length')))
        data = []
        for _ in range(0, compressed_data_length):
            data.append(await read_int(reader, 1))

        return CMD_SURVEY_RESULT(
            survey_id=survey_id,
            error=error,
            data=data,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [4]

        # survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(self.survey_id)

        # error: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.error)

        # compressed_data_length: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(len(self.data))

        # data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='compressed_data_length')))
        fmt += f'{len(self.data)}B'
        data.extend(self.data)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_XFER_INITIATE:

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        return CMD_XFER_INITIATE()

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [48]

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_XFER_DATA:
    data: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size = await read_int(reader, 2)

        # data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='size')))
        data = []
        for _ in range(0, size):
            data.append(await read_int(reader, 1))

        return CMD_XFER_DATA(
            data=data,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [49]

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(len(self.data))

        # data: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', content=<IntegerType.U8: 'U8'>), size=ArraySizeVariable(array_size_tag='Variable', size='size')))
        fmt += f'{len(self.data)}B'
        data.extend(self.data)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_XFER_ACCEPT:

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        return CMD_XFER_ACCEPT()

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [50]

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_XFER_RESUME:
    offset: int

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U64: 'U64'>)
        offset = await read_int(reader, 8)

        return CMD_XFER_RESUME(
            offset=offset,
        )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [51]

        # offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U64: 'U64'>)
        fmt += 'Q'
        data.append(self.offset)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_XFER_CANCEL:

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        return CMD_XFER_CANCEL()

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [52]

        data = struct.pack(fmt, *data)
        writer.write(data)


async def read_opcode_server(reader: asyncio.StreamReader):
    opcode = int.from_bytes(await reader.readexactly(1), 'little')
    if opcode == 0x00:
        return await CMD_AUTH_LOGON_CHALLENGE_Client.read(reader)
    if opcode == 0x01:
        return await CMD_AUTH_LOGON_PROOF_Client.read(reader)
    if opcode == 0x02:
        return await CMD_AUTH_RECONNECT_CHALLENGE_Client.read(reader)
    if opcode == 0x04:
        return await CMD_SURVEY_RESULT.read(reader)
    if opcode == 0x10:
        return await CMD_REALM_LIST_Client.read(reader)
    if opcode == 0x32:
        return await CMD_XFER_ACCEPT.read(reader)
    if opcode == 0x33:
        return await CMD_XFER_RESUME.read(reader)
    if opcode == 0x34:
        return await CMD_XFER_CANCEL.read(reader)
    else:
        raise Exception(f'incorrect opcode {opcode}')


async def read_opcode_client(reader: asyncio.StreamReader):
    opcode = int.from_bytes(await reader.readexactly(1), 'little')
    if opcode == 0x00:
        return await CMD_AUTH_LOGON_CHALLENGE_Server.read(reader)
    if opcode == 0x01:
        return await CMD_AUTH_LOGON_PROOF_Server.read(reader)
    if opcode == 0x10:
        return await CMD_REALM_LIST_Server.read(reader)
    if opcode == 0x30:
        return await CMD_XFER_INITIATE.read(reader)
    if opcode == 0x31:
        return await CMD_XFER_DATA.read(reader)
    else:
        raise Exception(f'incorrect opcode {opcode}')


