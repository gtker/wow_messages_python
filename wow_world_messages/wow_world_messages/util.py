import asyncio
import typing

import wow_srp

from wow_world_messages.wow_world_messages.vanilla import (
    CMSG_AUTH_SESSION,
    CMSG_CHAR_ENUM,
)

ClientOpcode = typing.Union[CMSG_AUTH_SESSION]


async def read_client_opcodes_unencrypted(reader: asyncio.StreamReader) -> ClientOpcode:
    opcode_size = 2
    size_field_size = 4

    size = int.from_bytes(await reader.readexactly(opcode_size), "big")
    opcode = int.from_bytes(await reader.readexactly(size_field_size), "little")

    if opcode == 0x1ED:
        return await CMSG_AUTH_SESSION.read(reader, size - size_field_size)
    else:
        raise Exception("unipml")


async def read_client_opcodes_encrypted(
    reader: asyncio.StreamReader,
    header_crypto: wow_srp.vanilla_header.HeaderCrypto,
) -> ClientOpcode:
    size_field_size = 4
    header_size = 6

    data = await reader.readexactly(header_size)

    size, opcode = header_crypto.decrypt_client_header(data)

    if opcode == 0x1ED:
        return await CMSG_AUTH_SESSION.read(reader, size - size_field_size)
    if opcode == 0x37:
        return await CMSG_CHAR_ENUM.read(reader, size - size_field_size)
    else:
        raise Exception(f"unipml 0x{opcode:02X}")


async def expect_client_opcode_unencrypted(
    reader: asyncio.StreamReader, opcode: typing.Type[ClientOpcode]
) -> typing.Optional[ClientOpcode]:
    o = await read_client_opcodes_unencrypted(reader)
    if isinstance(o, opcode):
        return o
    else:
        return None
