import model
from util import login_version_matches
from writer import Writer


def print_login_utils(s: Writer, messages: list[model.Container], v: int):
    if v == 0:
        return

    s.open("async def read_opcode_server(reader: asyncio.StreamReader):")
    s.wln("opcode = int.from_bytes(await reader.readexactly(1), 'little')")

    for e in messages:
        if not login_version_matches(e.tags, v):
            continue
        match e.object_type:
            case model.ObjectTypeClogin(opcode=opcode):
                s.open(f"if opcode == 0x{opcode:02X}:")
                s.wln(f"return await {e.name}.read(reader)")
                s.close()

    s.open("else:")
    s.wln("raise Exception(f'incorrect opcode {opcode}')")
    s.close()

    s.close()  # async def

    s.double_newline()

    s.open("async def read_opcode_client(reader: asyncio.StreamReader):")
    s.wln("opcode = int.from_bytes(await reader.readexactly(1), 'little')")

    for e in messages:
        if not login_version_matches(e.tags, v):
            continue
        match e.object_type:
            case model.ObjectTypeSlogin(opcode=opcode):
                s.open(f"if opcode == 0x{opcode:02X}:")
                s.wln(f"return await {e.name}.read(reader)")
                s.close()

    s.open("else:")
    s.wln("raise Exception(f'incorrect opcode {opcode}')")
    s.close()

    s.close()  # async def

    s.double_newline()
