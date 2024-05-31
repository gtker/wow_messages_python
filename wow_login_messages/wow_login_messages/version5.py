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
from .all import Version
from .version2 import TelemetryKey
from .all import CMD_AUTH_LOGON_CHALLENGE_Client
from .version2 import CMD_AUTH_RECONNECT_CHALLENGE_Server
from .all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from .version2 import CMD_AUTH_RECONNECT_PROOF_Client
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
    "RealmFlag",
    "SecurityFlag",
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
    "CMD_XFER_INITIATE",
    "CMD_XFER_DATA",
    "CMD_XFER_ACCEPT",
    "CMD_XFER_RESUME",
    "CMD_XFER_CANCEL",
    ]

class SecurityFlag(enum.Flag):
    NONE = 0
    PIN = 1
    MATRIX_CARD = 2


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
    async def read(reader: asyncio.StreamReader) -> Realm:
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
        width = None
        height = None
        digit_count = None
        challenge_count = None
        seed = None
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

            if SecurityFlag.PIN in security_flag:
                # pin_grid_seed: u32
                pin_grid_seed = await read_int(reader, 4)

                # pin_salt: u8[16]
                pin_salt = []
                for _ in range(0, 16):
                    pin_salt.append(await read_int(reader, 1))

            if SecurityFlag.MATRIX_CARD in security_flag:
                # width: u8
                width = await read_int(reader, 1)

                # height: u8
                height = await read_int(reader, 1)

                # digit_count: u8
                digit_count = await read_int(reader, 1)

                # challenge_count: u8
                challenge_count = await read_int(reader, 1)

                # seed: u64
                seed = await read_int(reader, 8)

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
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [0]

        _fmt += 'BB'
        _data.extend([0, self.result.value])
        if self.result == LoginResult.SUCCESS:
            _fmt += f'{len(self.server_public_key)}BB{len(self.generator)}BB{len(self.large_safe_prime)}B{len(self.salt)}B{len(self.crc_salt)}BB'
            _data.extend([*self.server_public_key, len(self.generator), *self.generator, len(self.large_safe_prime), *self.large_safe_prime, *self.salt, *self.crc_salt, self.security_flag.value])
            if SecurityFlag.PIN in self.security_flag:
                _fmt += f'I{len(self.pin_salt)}B'
                _data.extend([self.pin_grid_seed, *self.pin_salt])
            if SecurityFlag.MATRIX_CARD in self.security_flag:
                _fmt += 'BBBBQ'
                _data.extend([self.width, self.height, self.digit_count, self.challenge_count, self.seed])
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
    matrix_card_proof: typing.Optional[typing.List[int]] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> CMD_AUTH_LOGON_PROOF_Client:
        pin_salt = None
        pin_hash = None
        matrix_card_proof = None
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

        if SecurityFlag.PIN in security_flag:
            # pin_salt: u8[16]
            pin_salt = []
            for _ in range(0, 16):
                pin_salt.append(await read_int(reader, 1))

            # pin_hash: u8[20]
            pin_hash = []
            for _ in range(0, 20):
                pin_hash.append(await read_int(reader, 1))

        if SecurityFlag.MATRIX_CARD in security_flag:
            # matrix_card_proof: u8[20]
            matrix_card_proof = []
            for _ in range(0, 20):
                matrix_card_proof.append(await read_int(reader, 1))

        return CMD_AUTH_LOGON_PROOF_Client(
            client_public_key=client_public_key,
            client_proof=client_proof,
            crc_hash=crc_hash,
            telemetry_keys=telemetry_keys,
            security_flag=security_flag,
            pin_salt=pin_salt,
            pin_hash=pin_hash,
            matrix_card_proof=matrix_card_proof,
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

        if SecurityFlag.PIN in self.security_flag:
            _fmt += f'{len(self.pin_salt)}B{len(self.pin_hash)}B'
            _data.extend([*self.pin_salt, *self.pin_hash])
        if SecurityFlag.MATRIX_CARD in self.security_flag:
            _fmt += f'{len(self.matrix_card_proof)}B'
            _data.extend([*self.matrix_card_proof])
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
    unknown: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader) -> CMD_AUTH_LOGON_PROOF_Server:
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
    async def read(reader: asyncio.StreamReader) -> CMD_AUTH_RECONNECT_PROOF_Server:
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
    async def read(reader: asyncio.StreamReader) -> CMD_REALM_LIST_Server:
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
    if opcode == 0x03:
        return await CMD_AUTH_RECONNECT_PROOF_Client.read(reader)
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
    CMD_AUTH_RECONNECT_CHALLENGE_Server,
    CMD_AUTH_RECONNECT_PROOF_Server,
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
    if opcode == 0x02:
        return await CMD_AUTH_RECONNECT_CHALLENGE_Server.read(reader)
    if opcode == 0x03:
        return await CMD_AUTH_RECONNECT_PROOF_Server.read(reader)
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

