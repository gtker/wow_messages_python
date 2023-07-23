import asyncio
import dataclasses
import enum
import struct
import typing



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
        # major: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        major = int.from_bytes(await reader.readexactly(1), 'little')

        # minor: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        minor = int.from_bytes(await reader.readexactly(1), 'little')

        # patch: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        patch = int.from_bytes(await reader.readexactly(1), 'little')

        # build: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        build = int.from_bytes(await reader.readexactly(2), 'little')

        return Version(
            major=major,
            minor=minor,
            patch=patch,
            build=build,
        )

    def write(self, fmt, data):
        # major: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.major)

        # minor: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.minor)

        # patch: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        fmt += 'B'
        data.append(self.patch)

        # build: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(self.build)

        return fmt, data

    def _size(self):
        size = 0

        # major: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # minor: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # patch: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # build: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        return size


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
        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        protocol_version = ProtocolVersion(int.from_bytes(await reader.readexactly(1), 'little'))

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _size = int.from_bytes(await reader.readexactly(2), 'little')

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _game_name = int.from_bytes(await reader.readexactly(4), 'little')

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        version = await Version.read(reader)

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        platform = Platform(int.from_bytes(await reader.readexactly(4), 'little'))

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        os = Os(int.from_bytes(await reader.readexactly(4), 'little'))

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        locale = Locale(int.from_bytes(await reader.readexactly(4), 'little'))

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        utc_timezone_offset = int.from_bytes(await reader.readexactly(4), 'little')

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        client_ip_address = int.from_bytes(await reader.readexactly(4), 'big')

        # account_name: DataTypeString(data_type_tag='String')
        account_name = int.from_bytes(await reader.readexactly(1), 'little')
        account_name = (await reader.readexactly(account_name)).decode('utf-8')

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

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [0]

        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        fmt += 'B'
        data.append(self.protocol_version.value)

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(self._size())

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(5730135)

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        fmt, data = self.version.write(fmt, data)

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        fmt += 'I'
        data.append(self.platform.value)

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        fmt += 'I'
        data.append(self.os.value)

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        fmt += 'I'
        data.append(self.locale.value)

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(self.utc_timezone_offset)

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        fmt += 'I'
        data.append(self.client_ip_address)

        # account_name: DataTypeString(data_type_tag='String')
        fmt += f'B{len(self.account_name)}s'
        data.append(len(self.account_name))
        data.append(self.account_name.encode('utf-8'))

        data = struct.pack(fmt, *data)
        writer.write(data)

    def _size(self):
        size = 0

        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        size += 1

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        size += 5

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        size += 4

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        size += 4

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        size += 4

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        size += 4

        # account_name: DataTypeString(data_type_tag='String')
        size += len(self.account_name)

        return size - 3


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
        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        protocol_version = ProtocolVersion(int.from_bytes(await reader.readexactly(1), 'little'))

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _size = int.from_bytes(await reader.readexactly(2), 'little')

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _game_name = int.from_bytes(await reader.readexactly(4), 'little')

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        version = await Version.read(reader)

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        platform = Platform(int.from_bytes(await reader.readexactly(4), 'little'))

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        os = Os(int.from_bytes(await reader.readexactly(4), 'little'))

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        locale = Locale(int.from_bytes(await reader.readexactly(4), 'little'))

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        utc_timezone_offset = int.from_bytes(await reader.readexactly(4), 'little')

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        client_ip_address = int.from_bytes(await reader.readexactly(4), 'big')

        # account_name: DataTypeString(data_type_tag='String')
        account_name = int.from_bytes(await reader.readexactly(1), 'little')
        account_name = (await reader.readexactly(account_name)).decode('utf-8')

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

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [2]

        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        fmt += 'B'
        data.append(self.protocol_version.value)

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(self._size())

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(5730135)

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        fmt, data = self.version.write(fmt, data)

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        fmt += 'I'
        data.append(self.platform.value)

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        fmt += 'I'
        data.append(self.os.value)

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        fmt += 'I'
        data.append(self.locale.value)

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        fmt += 'I'
        data.append(self.utc_timezone_offset)

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        fmt += 'I'
        data.append(self.client_ip_address)

        # account_name: DataTypeString(data_type_tag='String')
        fmt += f'B{len(self.account_name)}s'
        data.append(len(self.account_name))
        data.append(self.account_name.encode('utf-8'))

        data = struct.pack(fmt, *data)
        writer.write(data)

    def _size(self):
        size = 0

        # protocol_version: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='ProtocolVersion', upcast=False))
        size += 1

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # game_name: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # version: DataTypeStruct(data_type_tag='Struct', content=DataTypeStructContent(sizes=Sizes(constant_sized=True, maximum_size=5, minimum_size=5), type_name='Version'))
        size += 5

        # platform: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Platform', upcast=False))
        size += 4

        # os: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Os', upcast=False))
        size += 4

        # locale: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U32: 'U32'>, type_name='Locale', upcast=False))
        size += 4

        # utc_timezone_offset: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # client_ip_address: DataTypeIPAddress(data_type_tag='IpAddress')
        size += 4

        # account_name: DataTypeString(data_type_tag='String')
        size += len(self.account_name)

        return size - 3


