import model
from util import login_version_matches
from writer import Writer


def print_login_utils(s: Writer, messages: list[model.Container], v: int):
    s.open("ClientOpcode = typing.Union[")

    for e in messages:
        if not login_version_matches(e.tags, v):
            continue

        match e.object_type:
            case model.ObjectTypeClogin():
                s.wln(f"{e.name},")

    s.close("]")  # ClientOpcode
    s.double_newline()

    s.open("async def read_client_opcode(reader: asyncio.StreamReader) -> typing.Optional[ClientOpcode]:")
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

    s.open(
        "async def expect_client_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ClientOpcode]) -> typing.Optional[ClientOpcode]:")
    s.wln("o = await read_client_opcode(reader)")

    s.open("if isinstance(o, opcode):")
    s.wln("return o")
    s.close()

    s.open("else:")
    s.wln("return None")
    s.close()

    s.close()
    s.double_newline()

    if v == 0:
        return

    s.open("ServerOpcode = typing.Union[")
    for e in messages:
        if not login_version_matches(e.tags, v):
            continue

        match e.object_type:
            case model.ObjectTypeSlogin():
                s.wln(f"{e.name},")

    s.close("]")  # ServerOpcode
    s.double_newline()

    s.open("async def read_server_opcode(reader: asyncio.StreamReader) -> typing.Optional[ServerOpcode]:")
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
    s.wln("return None")
    s.close()

    s.close()  # async def

    s.double_newline()

    s.open(
        "async def expect_server_opcode(reader: asyncio.StreamReader, opcode: typing.Type[ServerOpcode]) -> typing.Optional[ServerOpcode]:")
    s.wln("o = await read_server_opcode(reader)")

    s.open("if isinstance(o, opcode):")
    s.wln("return o")
    s.close()

    s.open("else:")
    s.wln("return None")
    s.close()

    s.close()
    s.newline()
