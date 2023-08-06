import asyncio
import struct
import typing


def packed_guid_size(value: int) -> int:
    size = 1
    for i in range(0, 8):
        if value & (0xFF << i * 8):
            size += 1
    return size


def packed_guid_write(
        value: int, fmt: str, data: list[typing.Any]
) -> (str, list[typing.Any]):
    fmt += "B"
    data.append(value)
    for i in range(0, 8):
        val = value & (0xFF << i * 8)
        if val:
            fmt += "B"
            data.append(val)

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
