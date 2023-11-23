from __future__ import annotations
import asyncio
import dataclasses
import enum
import struct
import typing

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
from .version2 import RealmFlag
from .version2 import Realm
from .all import Version
from .version2 import TelemetryKey
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .version2 import CMD_AUTH_LOGON_PROOF_Server
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from .version2 import CMD_REALM_LIST_Server
from .version2 import CMD_REALM_LIST_Client
from .version2 import CMD_XFER_INITIATE
from .version2 import CMD_XFER_DATA
from .version2 import CMD_XFER_ACCEPT
from .version2 import CMD_XFER_RESUME
from .version2 import CMD_XFER_CANCEL


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
    async def read(reader: asyncio.StreamReader) -> CMD_AUTH_LOGON_CHALLENGE_Server:
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

            # security_flag: SecurityFlag
            security_flag = SecurityFlag(await read_int(reader, 1))

            if security_flag == SecurityFlag.PIN:
                # pin_grid_seed: u32
                pin_grid_seed = await read_int(reader, 4)

                # pin_salt: u8[16]
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

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [0]

        _fmt += 'BB'
        _data.extend([0, self.result.value])
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.server_public_key)}BB{len(self.generator)}BB{len(self.large_safe_prime)}B{len(self.salt)}B{len(self.crc_salt)}BB'
            _data.extend([*self.server_public_key, len(self.generator), *self.generator, len(self.large_safe_prime), *self.large_safe_prime, *self.salt, *self.crc_salt, self.security_flag.value])
            if self.security_flag == SecurityFlag.PIN:
                _fmt += f'I{len(self.pin_salt)}B'
                _data.extend([self.pin_grid_seed, *self.pin_salt])
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
    security_flag: SecurityFlag
    pin_salt: typing.Optional[typing.List[int]] = None
    pin_hash: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> CMD_AUTH_LOGON_PROOF_Client:
        pin_salt = None
        pin_hash = None
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

        # security_flag: SecurityFlag
        security_flag = SecurityFlag(await read_int(reader, 1))

        if security_flag == SecurityFlag.PIN:
            # pin_salt: u8[16]
            pin_salt = []
            for _ in range(0, 16):
                pin_salt.append(await read_int(reader, 1))

            # pin_hash: u8[20]
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

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [1]

        _fmt += f'{len(self.client_public_key)}B{len(self.client_proof)}B{len(self.crc_hash)}BB'
        _data.extend([*self.client_public_key, *self.client_proof, *self.crc_hash, len(self.telemetry_keys)])
        # telemetry_keys: TelemetryKey[number_of_telemetry_keys]
        for i in self.telemetry_keys:
            _fmt, _data = i.write(_fmt, _data)

        # security_flag: SecurityFlag
        _fmt += 'B'
        _data.append(self.security_flag.value)

        if self.security_flag == SecurityFlag.PIN:
            _fmt += f'{len(self.pin_salt)}B{len(self.pin_hash)}B'
            _data.extend([*self.pin_salt, *self.pin_hash])
        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)


@dataclasses.dataclass
class CMD_SURVEY_RESULT:
    survey_id: int
    error: int
    data: typing.List[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> CMD_SURVEY_RESULT:
        # survey_id: u32
        survey_id = await read_int(reader, 4)

        # error: u8
        error = await read_int(reader, 1)

        # compressed_data_length: u16
        compressed_data_length = await read_int(reader, 2)

        # data: u8[compressed_data_length]
        data = []
        for _ in range(0, compressed_data_length):
            data.append(await read_int(reader, 1))

        return CMD_SURVEY_RESULT(
            survey_id=survey_id,
            error=error,
            data=data,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [4]

        _fmt += f'IBH{len(self.data)}B'
        _data.extend([self.survey_id, self.error, len(self.data), *self.data])
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
    CMD_SURVEY_RESULT,
    CMD_REALM_LIST_Client,
    CMD_XFER_ACCEPT,
    CMD_XFER_RESUME,
    CMD_XFER_CANCEL,
]


async def read_client_opcode(reader: asyncio.StreamReader) -> typing.Optional[ClientOpcode]:
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


async def expect_client_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ClientOpcode]) -> typing.Optional[ClientOpcode]:
    o = await read_client_opcode(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None


ServerOpcode = typing.Union[
    CMD_AUTH_LOGON_CHALLENGE_Server,
    CMD_AUTH_LOGON_PROOF_Server,
    CMD_REALM_LIST_Server,
    CMD_XFER_INITIATE,
    CMD_XFER_DATA,
]


async def read_server_opcode(reader: asyncio.StreamReader) -> typing.Optional[ServerOpcode]:
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
        return None


async def expect_server_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ServerOpcode]) -> typing.Optional[ServerOpcode]:
    o = await read_server_opcode(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None

