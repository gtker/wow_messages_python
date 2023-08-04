import model
from model import Container
from print_struct.print_size import print_size_inner
from print_struct.util import (
    integer_type_to_size,
    all_members_from_container,
    type_to_python_str,
)
from writer import Writer


def print_read_struct_member(s: Writer, d: model.Definition, container: model.Container):
    s.wln(f"# {d.name}: {d.data_type}")
    if d.tags.compressed is not None:
        s.wln("size = 0")

        for m in container.members:
            match m:
                case model.StructMemberDefinition(struct_member_content=model.Definition(name=name)):
                    if name == d.name:
                        break

            print_size_inner(s, m, False)

        s.wln(f"{d.name} = []")

        s.wln("for _ in range(size, body_size):")
        s.inc_indent()
        s.wln(f"{d.name}.append(int.from_bytes(await reader.readexactly(1), 'little'))")
        s.dec_indent()

        s.newline()
        return

    match d.data_type:
        case model.DataTypeInteger(content=content):
            size = integer_type_to_size(content)
            prefix = ""
            if d.constant_value is not None or d.size_of_fields_before_size is not None:
                prefix = "_"

            s.wln(
                f"{prefix}{d.name} = int.from_bytes(await reader.readexactly({size}), 'little')"
            )
        case model.DataTypeBool(content=content):
            size = integer_type_to_size(content)
            s.wln(
                f"{d.name} = int.from_bytes(await reader.readexactly({size}), 'little') == 1"
            )
        case model.DataTypeFlag(
            content=model.DataTypeFlagContent(
                type_name=type_name, integer_type=integer_type
            )
        ):
            size = integer_type_to_size(integer_type)
            s.wln(
                f"{d.name} = {type_name}(int.from_bytes(await reader.readexactly({size}), 'little'))"
            )
        case model.DataTypeEnum(content=content):
            size = integer_type_to_size(content.integer_type)
            s.wln(
                f"{d.name} = {content.type_name}(int.from_bytes(await reader.readexactly({size}), 'little'))"
            )
        case model.DataTypeString():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(1), 'little')")
            s.wln(f"{d.name} = (await reader.readexactly({d.name})).decode('utf-8')")

        case model.DataTypeCstring():
            s.wln(
                f"{d.name} = (await reader.readuntil(b'\\x00')).decode('utf-8').rstrip('\\x00')"
            )

        case model.DataTypeIPAddress():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(4), 'big')")

        case model.DataTypeArray(content=content):
            s.wln(f"{d.name} = []")
            match content.size:
                case model.ArraySizeFixed(size=size) | model.ArraySizeVariable(
                    size=size
                ):
                    s.wln(f"for _ in range(0, {size}):")
                case model.ArraySizeEndless():
                    s.wln("for _ in range(current_size, body_size):")
                case v:
                    raise Exception(f"{v}")
            s.inc_indent()

            match content.inner_type:
                case model.ArrayTypeInteger(content=content):
                    size = integer_type_to_size(content)
                    s.wln(
                        f"{d.name}.append(int.from_bytes(await reader.readexactly({size}), 'little'))"
                    )

                case model.ArrayTypeStruct(content=content):
                    s.wln(f"{d.name}.append(await {content.type_name}.read(reader))")

                case v:
                    raise Exception(f"{v}")

            s.dec_indent()

        case model.DataTypeStruct(
            content=model.DataTypeStructContent(type_name=type_name)
        ):
            s.wln(f"{d.name} = await {type_name}.read(reader)")
        case model.DataTypePopulation():
            s.wln(f"{d.name} = float.from_bytes(await reader.readexactly(4), 'little')")
        case model.DataTypeGUID():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(8), 'little')")
        case model.DataTypeLevel():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(1), 'little')")
        case model.DataTypeLevel16():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(2), 'little')")
        case model.DataTypeLevel32():
            s.wln(f"{d.name} = int.from_bytes(await reader.readexactly(4), 'little')")

        case model.DataTypeFloatingPoint():
            s.wln(f"[{d.name}] = struct.unpack('f', await reader.readexactly(4))")

        case v:
            raise Exception(f"{v}")

    s.newline()


def print_read_member(s: Writer, m: model.StructMember, container: model.Container):
    match m:
        case model.StructMemberDefinition(_tag, definition):
            print_read_struct_member(s, definition, container)

        case model.StructMemberIfStatement(_tag, statement):
            print_read_if_statement(s, statement, container, False)

        case model.StructMemberOptional(_tag, model.OptionalMembers(members=members)):
            for member in members:
                print_read_member(s, member, container)
            raise Exception("optional unimpl")

        case _:
            raise Exception("invalid struct member")


def print_read_if_statement(s: Writer, statement: model.IfStatement, container: model.Container, is_else_if: bool):
    extra_elseif = ""
    if is_else_if:
        extra_elseif = "el"

    original_type = type_to_python_str(statement.original_type)
    match statement.conditional.equations:
        case model.ConditionalEquationsEquals(
            _tag, model.ConditionalEquationsEqualsValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"{extra_elseif}if {statement.conditional.variable_name} == {original_type}.{value[0]}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsBitwiseAnd(
            values=model.ConditionalEquationsBitwiseAndValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"{extra_elseif}if {original_type}.{value[0]} in {statement.conditional.variable_name}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsNotEquals():
            raise Exception("unimpl")

    s.inc_indent()

    for member in statement.members:
        print_read_member(s, member, container)

    s.dec_indent()  # if

    for elseif in statement.else_if_statements:
        print_read_if_statement(s, elseif, container, True)

    if len(statement.else_members) != 0:
        s.wln("else:")
        s.inc_indent()

        for m in statement.else_members:
            print_read_member(s, m, container)

        s.dec_indent()



def print_read(s: Writer, container: Container):
    s.wln("@staticmethod")

    match container.object_type:
        case model.ObjectTypeCmsg() | model.ObjectTypeSmsg():
            s.wln("async def read(reader: asyncio.StreamReader, body_size: int):")
        case _:
            s.wln("async def read(reader: asyncio.StreamReader):")
    s.inc_indent()

    print_optional_names(s, container)

    if len(container.members) == 0:
        s.wln(f"return {container.name}()")
        s.dec_indent()
        s.newline()
        return

    for m in container.members:
        print_read_member(s, m, container)

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
