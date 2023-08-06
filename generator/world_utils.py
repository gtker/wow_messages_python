import model
from util import should_print_container, world_version_to_module_name
from writer import Writer


def print_type_unions(
        s: Writer, messages: list[model.Container], v: model.WorldVersion
):
    s.wln("ClientOpcode = typing.Union[")
    s.inc_indent()

    for e in messages:
        if not should_print_container(e, v):
            continue

        match e.object_type:
            case model.ObjectTypeCmsg() | model.ObjectTypeMsg():
                s.wln(f"{e.name},")
            case _:
                pass

    s.dec_indent()
    s.wln("]")

    s.newline()

    s.wln("ServerOpcode = typing.Union[")
    s.inc_indent()

    for e in messages:
        if not should_print_container(e, v):
            continue

        match e.object_type:
            case model.ObjectTypeSmsg() | model.ObjectTypeMsg():
                s.wln(f"{e.name},")
            case _:
                pass

    s.dec_indent()
    s.wln("]")

    s.newline()
    s.newline()


def expect_function(
        s: Writer, side: str, encryption: str, opcode: str, v: model.WorldVersion
):
    s.wln(f"async def expect_{side}_opcode_{encryption}(")
    s.inc_indent()
    s.wln("reader: asyncio.StreamReader,")
    s.wln(f"opcode: typing.Type[{opcode}],")
    if encryption == "encrypted":
        s.wln(
            f"header_crypto: wow_srp.{world_version_to_module_name(v)}_header.HeaderCrypto,"
        )
    s.dec_indent()
    s.wln(f") -> typing.Optional[{opcode}]:")

    s.inc_indent()
    extra = ""
    if encryption == "encrypted":
        extra = ", header_crypto"
    s.wln(f"o = await read_{side}_opcodes_{encryption}(reader{extra})")

    s.wln("if isinstance(o, opcode):")
    s.inc_indent()
    s.wln("return o")
    s.dec_indent()

    s.wln("else:")
    s.inc_indent()
    s.wln("return None")
    s.dec_indent()

    s.dec_indent()

    s.newline()
    s.newline()


def print_expects(s: Writer, v: model.WorldVersion):
    expect_function(s, "client", "unencrypted", "ClientOpcode", v)
    expect_function(s, "client", "encrypted", "ClientOpcode", v)

    expect_function(s, "server", "unencrypted", "ServerOpcode", v)
    expect_function(s, "server", "encrypted", "ServerOpcode", v)


def read_functions(
        s: Writer, v: model.WorldVersion, side: str, opcode: str, size_field_size: int
):
    s.wln(
        f"async def read_{side}_opcodes_unencrypted(reader: asyncio.StreamReader) -> {opcode}:"
    )
    s.inc_indent()

    s.wln("opcode_size = 2")
    s.wln(f"size_field_size = {size_field_size}")
    s.newline()

    s.wln('size = int.from_bytes(await reader.readexactly(opcode_size), "big")')
    s.wln(
        'opcode = int.from_bytes(await reader.readexactly(size_field_size), "little")'
    )

    s.wln(
        f"return await read_{side}_opcode_body(reader, opcode, size, size_field_size)"
    )
    s.dec_indent()  # async def read_

    s.newline()
    s.newline()

    s.wln(f"async def read_{side}_opcodes_encrypted(")
    s.inc_indent()

    s.wln("reader: asyncio.StreamReader,")
    s.wln(
        f"header_crypto: wow_srp.{world_version_to_module_name(v)}_header.HeaderCrypto,"
    )
    s.dec_indent()

    s.wln(f") -> {opcode}:")
    s.inc_indent()

    s.wln(f"size_field_size = {size_field_size}")
    s.wln(f"header_size = {size_field_size + 2}")

    s.newline()

    s.wln("data = await reader.readexactly(header_size)")
    s.newline()

    s.wln("size, opcode = header_crypto.decrypt_client_header(data)")
    s.newline()

    s.wln(
        f"return await read_{side}_opcode_body(reader, opcode, size, size_field_size)"
    )
    s.dec_indent()  # ) -> opcode

    s.newline()
    s.newline()


def print_reads(s: Writer, v: model.WorldVersion):
    read_functions(s, v, "client", "ClientOpcode", 4)
    read_functions(s, v, "server", "ServerOpcode", 2)


def print_read_body(s: Writer, messages: list[model.Container], v: model.WorldVersion):
    s.wln("async def read_client_opcode_body(")
    s.inc_indent()

    s.wln("reader: asyncio.StreamReader,")
    s.wln("opcode: int,")
    s.wln("size: int,")
    s.wln("size_field_size: int,")
    s.dec_indent()

    s.wln(") -> ClientOpcode:")
    s.inc_indent()
    s.wln("size = size - size_field_size")

    for e in messages:
        if not should_print_container(e, v):
            continue

        match e.object_type:
            case model.ObjectTypeCmsg(opcode=opcode) | model.ObjectTypeMsg(
                opcode=opcode
            ):
                s.wln(f"if opcode == 0x{opcode:04X}:")
                s.inc_indent()

                s.wln(f"return await {e.name}.read(reader, size)")
                s.dec_indent()
            case _:
                pass

    s.wln("else:")
    s.inc_indent()
    s.wln('raise Exception("unimplemented opcode 0x{opcode:02X}")')
    s.dec_indent()

    s.dec_indent()

    s.newline()
    s.newline()

    s.wln("async def read_server_opcode_body(")
    s.inc_indent()

    s.wln("reader: asyncio.StreamReader,")
    s.wln("opcode: int,")
    s.wln("size: int,")
    s.wln("size_field_size: int,")
    s.dec_indent()

    s.wln(") -> ServerOpcode:")
    s.inc_indent()
    s.wln("size = size - size_field_size")

    for e in messages:
        if not should_print_container(e, v):
            continue

        match e.object_type:
            case model.ObjectTypeSmsg(opcode=opcode) | model.ObjectTypeMsg(
                opcode=opcode
            ):
                s.wln(f"if opcode == 0x{opcode:04X}:")
                s.inc_indent()

                s.wln(f"return await {e.name}.read(reader, size)")
                s.dec_indent()
            case _:
                pass

    s.wln("else:")
    s.inc_indent()
    s.wln('raise Exception("unimplemented opcode 0x{opcode:02X}")')
    s.dec_indent()

    s.dec_indent()

    s.newline()
    s.newline()


def print_world_utils(
        s: Writer, messages: list[model.Container], v: model.WorldVersion
):
    print_type_unions(s, messages, v)

    print_read_body(s, messages, v)

    print_reads(s, v)

    print_expects(s, v)
