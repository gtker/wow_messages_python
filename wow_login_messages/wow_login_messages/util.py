import asyncio
import struct


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
