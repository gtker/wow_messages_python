import asyncio
import typing

from wow_login_messages.wow_login_messages.opcodes import (
    CMD_AUTH_LOGON_CHALLENGE_opcode,
    CMD_AUTH_LOGON_PROOF_opcode,
    CMD_REALM_LIST_opcode,
)
from wow_login_messages.wow_login_messages.version3 import (
    CMD_REALM_LIST_Client,
    CMD_AUTH_LOGON_CHALLENGE_Client,
    CMD_AUTH_LOGON_PROOF_Client,
    CMD_AUTH_RECONNECT_CHALLENGE_Client,
)


async def read_opcode_server(reader: asyncio.StreamReader):
    opcode = int.from_bytes(await reader.readexactly(1), "little")
    if opcode == CMD_AUTH_LOGON_CHALLENGE_opcode:
        return await CMD_AUTH_LOGON_CHALLENGE_Client.read(reader)
    elif opcode == CMD_AUTH_LOGON_PROOF_opcode:
        return await CMD_AUTH_LOGON_PROOF_Client.read(reader)
    elif opcode == CMD_REALM_LIST_opcode:
        return await CMD_REALM_LIST_Client.read(reader)
    else:
        raise Exception(f"incorrect opcode: {opcode}")


async def expect_login_or_reconnect(
    reader: asyncio.StreamReader,
) -> typing.Optional[CMD_AUTH_LOGON_CHALLENGE_Client]:
    opcode = await read_opcode_server(reader)
    match opcode:
        case CMD_AUTH_LOGON_CHALLENGE_Client():
            return opcode
        case CMD_AUTH_RECONNECT_CHALLENGE_Client():
            return opcode

    return None
