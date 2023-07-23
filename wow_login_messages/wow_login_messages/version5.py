import asyncio
import dataclasses
import enum
import struct
import typing

from all import Locale
from version2 import LoginResult
from all import Os
from all import Platform
from all import ProtocolVersion
from version2 import RealmCategory
from version2 import RealmType
from version3 import SecurityFlag
from version2 import RealmFlag
from version2 import TelemetryKey
from all import Version
from all import CMD_AUTH_LOGON_CHALLENGE_Client
from version3 import CMD_AUTH_LOGON_CHALLENGE_Server
from version3 import CMD_AUTH_LOGON_PROOF_Client
from all import CMD_AUTH_RECONNECT_CHALLENGE_Client
from version2 import CMD_AUTH_RECONNECT_CHALLENGE_Server
from version2 import CMD_AUTH_RECONNECT_PROOF_Client
from version2 import CMD_REALM_LIST_Client


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
    "TelemetryKey",
    "Version",
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
        # realm_type: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmType', upcast=False))
        realm_type = RealmType(int.from_bytes(await reader.readexactly(1), 'little'))

        # locked: DataTypeBool(data_type_tag='Bool', content=<IntegerType.U8: 'U8'>)
        locked = int.from_bytes(await reader.readexactly(1), 'little') == 1

        # flag: DataTypeFlag(data_type_tag='Flag', content=DataTypeFlagContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmFlag', upcast=False))
        flag = RealmFlag(int.from_bytes(await reader.readexactly(1), 'little'))

        # name: DataTypeCstring(data_type_tag='CString')
        name = (await reader.readuntil(b'\x00')).decode('utf-u8')

        # address: DataTypeCstring(data_type_tag='CString')
        address = (await reader.readuntil(b'\x00')).decode('utf-u8')

        # population: DataTypePopulation(data_type_tag='Population')
        population = float.from_bytes(await reader.readexactly(4), 'little')

        # number_of_characters_on_realm: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_characters_on_realm = int.from_bytes(await reader.readexactly(1), 'little')

        # category: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='RealmCategory', upcast=False))
        category = RealmCategory(int.from_bytes(await reader.readexactly(1), 'little'))

        # realm_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        realm_id = int.from_bytes(await reader.readexactly(1), 'little')

        return Realm(
            realm_type,
            locked,
            flag,
            name,
            address,
            population,
            number_of_characters_on_realm,
            category,
            realm_id,
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

        return fmt, data

    def _size(self):
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

        return size


@dataclasses.dataclass
class CMD_AUTH_LOGON_PROOF_Server:
    result: LoginResult
    server_proof: typing.Optional[typing.List[int]]
    hardware_survey_id: typing.Optional[int]
    unknown: typing.Optional[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_proof = None
        hardware_survey_id = None
        unknown = None
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        if result == LoginResult.SUCCESS:
            # server_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', inner_type=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            server_proof = []
            for _ in range(0, 20):
                server_proof.append(int.from_bytes(await reader.readexactly(1), 'little'))

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            hardware_survey_id = int.from_bytes(await reader.readexactly(4), 'little')

            # unknown: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            unknown = int.from_bytes(await reader.readexactly(2), 'little')

        return CMD_AUTH_LOGON_PROOF_Server(
            result,
            server_proof,
            hardware_survey_id,
            unknown,
            )

    def write(self, writer: asyncio.StreamWriter):
        fmt = '<B' # opcode
        data = [1]

        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        fmt += 'B'
        data.append(self.result.value)

        if self.result == LoginResult.SUCCESS:
            # server_proof: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeInteger(array_type_tag='Integer', inner_type=<IntegerType.U8: 'U8'>), size=ArraySizeFixed(array_size_tag='Fixed', size='20')))
            fmt += f'{len(self.server_proof)}B'
            data.extend(self.server_proof)

            # hardware_survey_id: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
            fmt += 'I'
            data.append(self.hardware_survey_id)

            # unknown: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
            fmt += 'H'
            data.append(self.unknown)

        data = struct.pack(fmt, *data)
        writer.write(data)


@dataclasses.dataclass
class CMD_AUTH_RECONNECT_PROOF_Server:
    result: LoginResult

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        # result: DataTypeEnum(data_type_tag='Enum', content=DataTypeEnumContent(integer_type=<IntegerType.U8: 'U8'>, type_name='LoginResult', upcast=False))
        result = LoginResult(int.from_bytes(await reader.readexactly(1), 'little'))

        # padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _padding = int.from_bytes(await reader.readexactly(2), 'little')

        return CMD_AUTH_RECONNECT_PROOF_Server(
            result,
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
        _size = int.from_bytes(await reader.readexactly(2), 'little')

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        _header_padding = int.from_bytes(await reader.readexactly(4), 'little')

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        number_of_realms = int.from_bytes(await reader.readexactly(1), 'little')

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        realms = []
        for _ in range(0, number_of_realms):
            realms.append(await Realm.read(reader))

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        _footer_padding = int.from_bytes(await reader.readexactly(2), 'little')

        return CMD_REALM_LIST_Server(
            realms,
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

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            fmt, data = i.write(fmt, data)

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        fmt += 'H'
        data.append(0)

        data = struct.pack(fmt, *data)
        writer.write(data)

    def _size(self):
        size = 0

        # size: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        # header_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U32: 'U32'>)
        size += 4

        # number_of_realms: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U8: 'U8'>)
        size += 1

        # realms: DataTypeArray(data_type_tag='Array', content=Array(inner_type=ArrayTypeStruct(array_type_tag='Struct', inner_type='Realm'), size=ArraySizeVariable(array_size_tag='Variable', size='number_of_realms')))
        for i in self.realms:
            size += i._size()

        # footer_padding: DataTypeInteger(data_type_tag='Integer', content=<IntegerType.U16: 'U16'>)
        size += 2

        return size - 2


