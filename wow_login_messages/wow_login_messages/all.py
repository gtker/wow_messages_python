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



__all__ = [
    "Locale",
    "Os",
    "Platform",
    "ProtocolVersion",
    "Version",
    "CMD_AUTH_LOGON_CHALLENGE_Client",
    "CMD_AUTH_RECONNECT_CHALLENGE_Client",
    ]

class Locale(enum.Enum):
    EN_GB = 1701726018
    EN_US = 1701729619
    ES_MX = 1702055256
    PT_BR = 1886667346
    FR_FR = 1718765138
    DE_DE = 1684358213
    ES_ES = 1702053203
    PT_PT = 1886670932
    IT_IT = 1769228628
    RU_RU = 1920291413
    KO_KR = 1802455890
    ZH_TW = 2053657687
    EN_TW = 1701729367
    EN_CN = 1701725006


class Os(enum.Enum):
    WINDOWS = 5728622
    MAC_OS_X = 5198680


class Platform(enum.Enum):
    X86 = 7878710
    POWER_PC = 5263427


class ProtocolVersion(enum.Enum):
    TWO = 2
    THREE = 3
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


@dataclasses.dataclass
class Version:
    major: int
    minor: int
    patch: int
    build: int

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # major: u8
        major = await read_int(reader, 1)

        # minor: u8
        minor = await read_int(reader, 1)

        # patch: u8
        patch = await read_int(reader, 1)

        # build: u16
        build = await read_int(reader, 2)

        return Version(
            major=major,
            minor=minor,
            patch=patch,
            build=build,
        )

    def write(self, _fmt, _data):
        _fmt += 'BBBH'
        _data.extend([self.major, self.minor, self.patch, self.build])
        return _fmt, _data


@dataclasses.dataclass
class CMD_AUTH_LOGON_CHALLENGE_Client:
    protocol_version: ProtocolVersion
    version: Version
    platform: Platform
    os: Os
    locale: Locale
    utc_timezone_offset: int
    client_ip_address: int
    account_name: str

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # protocol_version: ProtocolVersion
        protocol_version = ProtocolVersion(await read_int(reader, 1))

        # size: u16
        _size = await read_int(reader, 2)

        # game_name: u32
        _game_name = await read_int(reader, 4)

        # version: Version
        version = await Version.read(reader)

        # platform: Platform
        platform = Platform(await read_int(reader, 4))

        # os: Os
        os = Os(await read_int(reader, 4))

        # locale: Locale
        locale = Locale(await read_int(reader, 4))

        # utc_timezone_offset: u32
        utc_timezone_offset = await read_int(reader, 4)

        # client_ip_address: IpAddress
        client_ip_address = await read_int(reader, 4)

        # account_name: String
        account_name = await read_string(reader)

        return CMD_AUTH_LOGON_CHALLENGE_Client(
            protocol_version=protocol_version,
            version=version,
            platform=platform,
            os=os,
            locale=locale,
            utc_timezone_offset=utc_timezone_offset,
            client_ip_address=client_ip_address,
            account_name=account_name,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [0]

        _fmt += 'BHI'
        _data.extend([self.protocol_version.value, self.size(), 5730135])
        # version: Version
        _fmt, _data = self.version.write(_fmt, _data)

        # platform: Platform
        _fmt += 'I'
        _data.append(self.platform.value)

        # os: Os
        _fmt += 'I'
        _data.append(self.os.value)

        # locale: Locale
        _fmt += 'I'
        _data.append(self.locale.value)

        # utc_timezone_offset: u32
        _fmt += 'I'
        _data.append(self.utc_timezone_offset)

        # client_ip_address: IpAddress
        _fmt += 'I'
        _data.append(self.client_ip_address)

        # account_name: String
        _fmt += f'B{len(self.account_name)}s'
        _data.extend([len(self.account_name), self.account_name.encode('utf-8')])

        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)

    def size(self) -> int:
        return 30 + len(self.account_name)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_CHALLENGE_Client:
    protocol_version: ProtocolVersion
    version: Version
    platform: Platform
    os: Os
    locale: Locale
    utc_timezone_offset: int
    client_ip_address: int
    account_name: str

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # protocol_version: ProtocolVersion
        protocol_version = ProtocolVersion(await read_int(reader, 1))

        # size: u16
        _size = await read_int(reader, 2)

        # game_name: u32
        _game_name = await read_int(reader, 4)

        # version: Version
        version = await Version.read(reader)

        # platform: Platform
        platform = Platform(await read_int(reader, 4))

        # os: Os
        os = Os(await read_int(reader, 4))

        # locale: Locale
        locale = Locale(await read_int(reader, 4))

        # utc_timezone_offset: u32
        utc_timezone_offset = await read_int(reader, 4)

        # client_ip_address: IpAddress
        client_ip_address = await read_int(reader, 4)

        # account_name: String
        account_name = await read_string(reader)

        return CMD_AUTH_RECONNECT_CHALLENGE_Client(
            protocol_version=protocol_version,
            version=version,
            platform=platform,
            os=os,
            locale=locale,
            utc_timezone_offset=utc_timezone_offset,
            client_ip_address=client_ip_address,
            account_name=account_name,
        )

    def write(self, writer: typing.Union[asyncio.StreamWriter, bytearray]):
        _fmt = '<B' # opcode
        _data = [2]

        _fmt += 'BHI'
        _data.extend([self.protocol_version.value, self.size(), 5730135])
        # version: Version
        _fmt, _data = self.version.write(_fmt, _data)

        # platform: Platform
        _fmt += 'I'
        _data.append(self.platform.value)

        # os: Os
        _fmt += 'I'
        _data.append(self.os.value)

        # locale: Locale
        _fmt += 'I'
        _data.append(self.locale.value)

        # utc_timezone_offset: u32
        _fmt += 'I'
        _data.append(self.utc_timezone_offset)

        # client_ip_address: IpAddress
        _fmt += 'I'
        _data.append(self.client_ip_address)

        # account_name: String
        _fmt += f'B{len(self.account_name)}s'
        _data.extend([len(self.account_name), self.account_name.encode('utf-8')])

        _data = struct.pack(_fmt, *_data)
        if isinstance(writer, bytearray):
            for i in range(0, len(_data)):
                writer[i] = _data[i]
            return
        writer.write(_data)

    def size(self) -> int:
        return 30 + len(self.account_name)


ClientOpcode = typing.Union[
    CMD_AUTH_LOGON_CHALLENGE_Client,
    CMD_AUTH_RECONNECT_CHALLENGE_Client,
    ]


async def read_client_opcode(reader: asyncio.StreamReader) -> typing.Optional[ClientOpcode]:
    opcode = int.from_bytes(await reader.readexactly(1), 'little')
    if opcode == 0x00:
        return await CMD_AUTH_LOGON_CHALLENGE_Client.read(reader)
    if opcode == 0x02:
        return await CMD_AUTH_RECONNECT_CHALLENGE_Client.read(reader)
    else:
        raise Exception(f'incorrect opcode {opcode}')


async def expect_client_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ClientOpcode]) -> typing.Optional[ClientOpcode]:
    o = await read_client_opcode(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None


