import asyncio
import dataclasses
import struct
import typing


@dataclasses.dataclass
class EnchantMask:
    fields: dict[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        mask = await read_int(reader, 2)

        fields = {}
        for index in range(0, 16):
            if mask & 1 << index:
                data = await read_int(reader, 2)
                fields[index] = data

        return EnchantMask(fields=fields)

    def write(self, fmt, data):
        mask = 0
        for i, _ in enumerate(self.fields):
            mask |= 1 << i

        fmt += 'H'
        data.append(mask)

        for d in self.fields:
            fmt += "H"
            data.append(d)

        return fmt, data

    def size(self):
        return 2 + len(self.fields) * 2


def packed_guid_size(value: int) -> int:
    size = 1
    for i in range(0, 8):
        if value & (0xFF << i * 8):
            size += 1
    return size


def packed_guid_write(
        value: int,
        fmt: str,
        data: list[typing.Any]
) -> (str, list[typing.Any]):
    mask = 0
    for i in range(0, 8):
        val = value & (0xFF << i * 8)
        if val != 0:
            mask |= 1 << i

    fmt += "B"
    data.append(mask)
    for i in range(0, 8):
        val = value & (0xFF << i * 8)
        if val != 0:
            fmt += "B"
            data.append(val >> i * 8)

    return fmt, data


async def read_packed_guid(reader: asyncio.StreamReader) -> int:
    value = 0
    byte_mask = int.from_bytes(await reader.readexactly(1), "little")
    for i in range(0, 8):
        if byte_mask & (1 << i):
            value |= int.from_bytes(await reader.readexactly(1), "little") << (i * 8)

    return value


async def read_int(reader: asyncio.StreamReader, size: int) -> int:
    return int.from_bytes(await reader.readexactly(size), "little")


async def read_bool(reader: asyncio.StreamReader, size: int) -> bool:
    return await read_int(reader, size) == 1


async def read_string(reader: asyncio.StreamReader) -> str:
    length = await read_int(reader, 1)
    return (await reader.readexactly(length)).decode("utf-8")


async def read_cstring(reader: asyncio.StreamReader) -> str:
    return (await reader.readuntil(b'\x00')).decode("utf-8").rstrip('\x00')


async def read_sized_cstring(reader: asyncio.StreamReader) -> str:
    length = await read_int(reader, 4)
    return (await reader.readexactly(length)).decode("utf-8").rstrip('\x00')


async def read_float(reader: asyncio.StreamReader) -> float:
    [value] = struct.unpack('f', await reader.readexactly(4))
    return value
