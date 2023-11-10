import model
from model import Container
from print_struct.util import (
    integer_type_to_size,
    all_members_from_container,
    print_if_statement_header, type_to_wowm_str,
)
from util import container_needs_size_in_read
from writer import Writer


def print_read_struct_member(s: Writer, d: model.Definition, needs_size: bool, container_is_compressed: bool):
    s.wln(f"# {d.name}: {type_to_wowm_str(d.data_type)}")
    match d.data_type:
        case model.DataTypeInteger(content=integer_type):
            size = integer_type_to_size(integer_type)
            prefix = ""
            if d.constant_value is not None or d.size_of_fields_before_size is not None:
                prefix = "_"

            s.wln(
                f"{prefix}{d.name} = await read_int(reader, {size})"
            )

            if needs_size:
                s.wln(f"_size += {size}")
        case model.DataTypeBool(content=integer_type):
            size = integer_type_to_size(integer_type)
            s.wln(
                f"{d.name} = await read_bool(reader, {size})"
            )

            if needs_size:
                s.wln(f"_size += {size}")

        case model.DataTypeFlag(
            content=model.DataTypeFlagContent(
                type_name=type_name, integer_type=integer_type
            )
        ):
            size = integer_type_to_size(integer_type)
            s.wln(
                f"{d.name} = {type_name}(await read_int(reader, {size}))"
            )

            if needs_size:
                s.wln(f"_size += {size}")

        case model.DataTypeEnum(content=integer_type):
            size = integer_type_to_size(integer_type.integer_type)
            s.wln(
                f"{d.name} = {integer_type.type_name}(await read_int(reader, {size}))"
            )

            if needs_size:
                s.wln(f"_size += {size}")

        case model.DataTypeString():
            s.wln(f"{d.name} = await read_string(reader)")

            if needs_size:
                s.wln(f"_size += len({d.name}) + 1")

        case model.DataTypeCstring():
            s.wln(
                f"{d.name} = await read_cstring(reader)"
            )

            if needs_size:
                s.wln(f"_size += len({d.name}) + 1")

        case model.DataTypeSizedCstring():
            s.wln(f"{d.name} = await read_sized_cstring(reader)")

            if needs_size:
                s.wln(f"_size += len({d.name}) + 5")

        case model.DataTypeDateTime() | model.DataTypeGold() | model.DataTypeSeconds() | model.DataTypeMilliseconds() | model.DataTypeIPAddress():
            s.wln(f"{d.name} = await read_int(reader, 4)")

            if needs_size:
                s.wln(f"_size += 4")

        case model.DataTypeGUID():
            s.wln(f"{d.name} = await read_int(reader, 8)")

            if needs_size:
                s.wln(f"_size += 8")

        case model.DataTypeLevel():
            s.wln(f"{d.name} = await read_int(reader, 1)")

            if needs_size:
                s.wln(f"_size += 1")

        case model.DataTypeLevel16() | model.DataTypeSpell16():
            s.wln(f"{d.name} = await read_int(reader, 2)")

            if needs_size:
                s.wln(f"_size += 2")
        case model.DataTypeLevel32() | model.DataTypeSpell() | model.DataTypeItem():
            s.wln(f"{d.name} = await read_int(reader, 4)")

            if needs_size:
                s.wln(f"_size += 4")

        case model.DataTypePopulation():
            s.wln(f"{d.name} = await read_float(reader)")

            if needs_size:
                s.wln(f"_size += 4")

        case model.DataTypePackedGUID():
            s.wln(f"{d.name} = await read_packed_guid(reader)")

            if needs_size:
                s.wln(f"_size += packed_guid_size({d.name})")

        case model.DataTypeFloatingPoint():
            s.wln(f"{d.name} = await read_float(reader)")

            if needs_size:
                s.wln(f"_size += 4")

        case model.DataTypeStruct(
            content=model.DataTypeStructContent(struct_data=e)
        ):
            s.wln(f"{d.name} = await {e.name}.read(reader)")

            if needs_size:
                if e.sizes.constant_sized:
                    s.wln(f"_size += {e.sizes.maximum_size}")
                else:
                    s.wln(f"_size += {d.name}.size()")

        case model.DataTypeUpdateMask():
            s.wln(f"{d.name} = await UpdateMask.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeAuraMask():
            s.wln(f"{d.name} = await AuraMask.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeMonsterMoveSpline():
            s.wln(f"{d.name} = await MonsterMoveSpline.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeEnchantMask():
            s.wln(f"{d.name} = await EnchantMask.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeNamedGUID():
            s.wln(f"{d.name} = await NamedGuid.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeInspectTalentGearMask():
            s.wln(f"{d.name} = await InspectTalentGearMask.read(reader)")

            if needs_size:
                s.wln(f"_size += {d.name}.size()")

        case model.DataTypeArray(content=array):
            reader = "reader"
            if array.compressed:
                s.wln("# {d.name}_decompressed_size: u32")
                s.wln("_size += 4  # decompressed_size")
                s.newline()

                s.wln(f"{d.name}_decompressed_size = await read_int(reader, 4)")

                s.wln(f"{d.name}_bytes = await reader.readexactly(body_size - _size)")
                s.newline()

                s.wln(f"{d.name}_reader = reader")
                s.open(f"if len({d.name}_bytes) != 0:")
                s.wln(f"{d.name}_bytes = zlib.decompress({d.name}_bytes, bufsize={d.name}_decompressed_size)")
                s.wln(f"{d.name}_reader = asyncio.StreamReader()")
                s.wln(f"{d.name}_reader.feed_data({d.name}_bytes)")
                s.wln(f"{d.name}_reader.feed_eof()")
                s.close()

                s.newline()
                reader = f"{d.name}_reader"

            s.wln(f"{d.name} = []")
            match array.size:
                case model.ArraySizeFixed(size=size) | model.ArraySizeVariable(
                    size=size
                ):
                    s.open(f"for _ in range(0, {size}):")
                case model.ArraySizeEndless():
                    if container_is_compressed:
                        s.open(f"while not reader.at_eof():")
                    elif not array.compressed:
                        s.open("while _size < body_size:")
                    else:
                        s.open(f"while not {d.name}_reader.at_eof():")
                case v:
                    raise Exception(f"{v}")

            match array.inner_type:
                case model.ArrayTypeInteger(content=integer_type):
                    size = integer_type_to_size(integer_type)
                    s.wln(
                        f"{d.name}.append(await read_int({reader}, {size}))"
                    )

                case model.ArrayTypeStruct(content=model.ArrayTypeStructContent(struct_data=e)):
                    s.wln(f"{d.name}.append(await {e.name}.read({reader}))")

                case model.ArrayTypeCstring():
                    s.wln(
                        f"{d.name}.append(await read_cstring({reader}))"
                    )

                case model.ArrayTypeGUID():
                    s.wln(
                        f"{d.name}.append(await read_int({reader}, 8))"
                    )

                case model.ArrayTypeSpell():
                    s.wln(
                        f"{d.name}.append(await read_int({reader}, 4))"
                    )

                case model.ArrayTypePackedGUID():
                    s.wln(
                        f"{d.name}.append(await read_packed_guid({reader}))"
                    )

                case v:
                    raise Exception(f"{v}")

            if needs_size or isinstance(array.size, model.ArraySizeEndless):
                s.w("_size += ")
                match array.inner_type:
                    case model.ArrayTypeInteger(content=integer_type):
                        size = integer_type_to_size(integer_type)
                        s.wln_no_indent(str(size))
                    case model.ArrayTypeStruct(content=model.ArrayTypeStructContent(struct_data=e)):
                        if e.sizes.constant_sized:
                            s.wln_no_indent(str(e.sizes.maximum_size))
                        else:
                            s.wln_no_indent(f"{d.name}[-1].size()")

                    case model.ArrayTypeCstring():
                        s.wln_no_indent(f"len({d.name}[-1]) + 1")

                    case model.ArrayTypeGUID():
                        s.wln_no_indent(str(8))

                    case model.ArrayTypeSpell():
                        s.wln_no_indent(str(4))

                    case model.ArrayTypePackedGUID():
                        s.wln_no_indent(f"{d.name}[-1].size()")

                    case v:
                        raise Exception(f"{v}")

            s.dec_indent()

        case v:
            raise Exception(f"{v}")

    s.newline()


def print_read_member(s: Writer, m: model.StructMember, container: model.Container, needs_size: bool):
    match m:
        case model.StructMemberDefinition(_tag, definition):
            print_read_struct_member(s, definition, needs_size, container.tags.compressed)

        case model.StructMemberIfStatement(_tag, statement):
            print_read_if_statement(s, statement, container, False, needs_size)

        case model.StructMemberOptional(_tag, model.OptionalMembers(name=name, members=members)):
            s.wln(f"# {name}: optional")
            s.open("if _size < body_size:")

            for member in members:
                print_read_member(s, member, container, needs_size)

            s.close()

        case _:
            raise Exception("invalid struct member")


def print_read_if_statement(
        s: Writer,
        statement: model.IfStatement,
        container: model.Container,
        is_else_if: bool,
        needs_size: bool,
):
    extra_elseif = ""
    if is_else_if:
        extra_elseif = "el"

    print_if_statement_header(s, statement, extra_elseif, "")

    s.inc_indent()

    for member in statement.members:
        print_read_member(s, member, container, needs_size)

    s.dec_indent()  # if

    for elseif in statement.else_if_statements:
        print_read_if_statement(s, elseif, container, True, needs_size)

    if len(statement.else_members) != 0:
        s.wln("else:")
        s.inc_indent()

        for m in statement.else_members:
            print_read_member(s, m, container, needs_size)

        s.dec_indent()


def print_read(s: Writer, container: Container):
    s.wln("@staticmethod")

    match container.object_type:
        case model.ObjectTypeCmsg() | model.ObjectTypeSmsg() | model.ObjectTypeMsg():
            s.wln(f"async def read(reader: asyncio.StreamReader, body_size: int) -> {container.name}:")
        case _:
            s.wln(f"async def read(reader: asyncio.StreamReader) -> {container.name}:")
    s.inc_indent()

    print_optional_names(s, container)

    if len(container.members) == 0:
        s.wln(f"return {container.name}()")
        s.dec_indent()
        s.newline()
        return

    if container.tags.compressed:
        s.write_block("""
decompressed_size = await read_int(reader, 4)
compressed_bytes = await reader.readexactly(body_size - 4)
decompressed_bytes = zlib.decompress(compressed_bytes, bufsize=decompressed_size)
reader = asyncio.StreamReader()
reader.feed_data(decompressed_bytes)
reader.feed_eof()
        """)
        s.newline()

    needs_size = container_needs_size_in_read(container)

    if needs_size:
        s.wln("_size = 0")
        s.newline()

    for m in container.members:
        print_read_member(s, m, container, needs_size)

    s.wln(f"return {container.name}(")
    s.inc_indent()
    for d in all_members_from_container(container):
        if (
                d.used_as_size_in is not None
                or d.size_of_fields_before_size is not None
                or d.constant_value is not None
        ):
            continue
        s.wln(f"{d.name}={d.name},")
    s.dec_indent()  # return container name
    s.wln(")")

    s.dec_indent()  # read
    s.newline()


def print_optional_names(s: Writer, container: Container):
    def traverse(s: Writer, m: model.StructMember, should_print: bool):
        def traverse_if_statement(s: Writer, statement: model.IfStatement):
            for m in statement.members:
                traverse(s, m, True)

            for elseif in statement.else_if_statements:
                traverse_if_statement(s, elseif)

            for m in statement.else_members:
                traverse(s, m, True)

        match m:
            case model.StructMemberDefinition(struct_member_content=d):
                if should_print:
                    s.wln(f"{d.name} = None")
            case model.StructMemberIfStatement(struct_member_content=statement):
                traverse_if_statement(s, statement)
            case model.StructMemberOptional(struct_member_content=optional):
                for m in optional.members:
                    traverse(s, m, True)

    for m in container.members:
        traverse(s, m, False)
