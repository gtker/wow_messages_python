import typing

import model
from print_struct.util import (
    integer_type_to_size,
    print_if_statement_header,
)
from writer import Writer


def print_size(s: Writer, container: model.Container):
    match container.object_type:
        case model.ObjectTypeCmsg() | model.ObjectTypeSmsg() | model.ObjectTypeMsg() | model.ObjectTypeStruct():
            if container.sizes.constant_sized:
                return
        case _:
            if container.manual_size_subtraction is None:
                return

    s.wln("def _size(self) -> int:")
    s.inc_indent()

    if container.sizes.constant_sized:
        s.wln(f"return {container.sizes.maximum_size}")
        s.dec_indent()
        return

    all_addable = True
    sizes = []
    count = 0
    for d in container.members:
        match d:
            case model.StructMemberDefinition(struct_member_content=d):
                addable = addable_size_value(d.data_type, "self.", d.name)
                if addable is not None:
                    if isinstance(addable, int):
                        count += addable
                    elif isinstance(addable, str):
                        sizes.append(addable)
                    else:
                        raise Exception("invalid type")
                else:
                    all_addable = False
                    break
            case _:
                all_addable = False

    extra_return = ""
    if container.manual_size_subtraction is not None:
        extra_return = f" - {container.manual_size_subtraction}"

    if all_addable:
        if len(sizes) != 0:
            s.wln(f"return {count} + {' + '.join(sizes)}{extra_return}")
        else:
            s.wln(f"return {count}{extra_return}")

    else:
        s.wln("size = 0")
        s.newline()

        for m in container.members:
            print_size_inner(s, m, True)

        s.wln(f"return size{extra_return}")

    s.dec_indent()
    s.newline()


def array_size_inner_values(
        array: model.Array, name: str, extra_self: str
) -> typing.Optional[typing.Union[str, int]]:
    size = 0
    match array.inner_type:
        case model.ArrayTypeGUID():
            size = 8
        case model.ArrayTypeStruct(content=content):
            if content.sizes.constant_sized:
                size = content.sizes.maximum_size
            else:
                return None
        case model.ArrayTypeInteger(content=integer_type):
            size = integer_type_to_size(integer_type)
        case _:
            return None

    match array.size:
        case model.ArraySizeFixed(size=array_size):
            return size * int(array_size)
        case model.ArraySizeVariable(size=array_size):
            return f"{size} * len({extra_self}{name})"


def addable_size_value(
        data_type: model.DataType, extra_self: str, name: str
) -> typing.Optional[typing.Union[str, int]]:
    value = direct_size_value(data_type, name, extra_self)
    if value is not None:
        return value

    match data_type:
        case model.DataTypeStruct(content=content):
            if not content.sizes.constant_sized:
                return f"{extra_self}{name}._size()"
        case model.DataTypeString():
            return f"len({extra_self}{name})"
        case model.DataTypeCstring():
            return f"len({extra_self}{name}) + 1"
        case model.DataTypeSizedCstring():
            return f"len({extra_self}{name}) + 5"
        case model.DataTypePackedGUID():
            return f"packed_guid_size({extra_self}{name})"
        case model.DataTypeArray(content=array):
            size = array_size_inner_values(array, name, extra_self)
            if isinstance(size, str) or isinstance(size, int):
                return size

    return None


def direct_size_value(
        data_type: model.DataType, name: str, extra_self: str
) -> typing.Optional[int]:
    match data_type:
        case model.DataTypeInteger(content=integer_type):
            return integer_type_to_size(integer_type)
        case model.DataTypeBool(content=integer_type):
            return integer_type_to_size(integer_type)
        case model.DataTypeEnum(content=content):
            return integer_type_to_size(content.integer_type)
        case model.DataTypeFlag(content=content):
            return integer_type_to_size(content.integer_type)

        case model.DataTypeStruct(content=content):
            if content.sizes.constant_sized:
                return content.sizes.maximum_size

        case model.DataTypeDateTime() | model.DataTypeGold() | model.DataTypeSeconds() | model.DataTypeMilliseconds() | model.DataTypeIPAddress():
            return 4
        case model.DataTypePopulation():
            return 4
        case model.DataTypeGUID():
            return 8
        case model.DataTypeLevel():
            return 1
        case model.DataTypeLevel16():
            return 2
        case model.DataTypeLevel32():
            return 4

        case model.DataTypeFloatingPoint():
            return 4

        case model.DataTypeArray(content=array):
            size = array_size_inner_values(array, name, extra_self)
            if isinstance(size, int):
                return size

    return None


def print_size_inner(s: Writer, m: model.StructMember, with_self: bool):
    extra_self = ""
    if with_self:
        extra_self = "self."

    match m:
        case model.StructMemberDefinition(struct_member_content=d):
            s.wln(f"# {d.name}: {d.data_type}")
            addable = addable_size_value(d.data_type, extra_self, d.name)
            if addable is not None:
                s.wln(f"size += {addable}")
                s.newline()
                return

            match d.data_type:
                case model.DataTypeArray(content=array):
                    if d.tags.compressed is not None:
                        s.wln(f"size += len({extra_self}{d.name})")
                    else:
                        s.wln(f"for i in {extra_self}{d.name}:")
                        s.inc_indent()

                        match array.inner_type:
                            case model.ArrayTypeStruct(content=content):
                                if content.sizes.constant_sized:
                                    s.wln(f"size += {content.sizes.maximum_size}")
                                else:
                                    s.wln("size += i._size()")
                            case model.ArrayTypeCstring():
                                s.wln("size += len(i) + 1")
                            case v:
                                raise Exception(f"{v}")

                        s.dec_indent()

                case v:
                    raise Exception(f"{v}")

        case model.StructMemberIfStatement(struct_member_content=statement):
            print_size_if_statement(s, statement, False, with_self)
        case model.StructMemberOptional():
            raise Exception("unimpl")
        case v:
            raise Exception(f"{v}")

    s.newline()


def print_size_if_statement(
        s: Writer, statement: model.IfStatement, is_else_if: bool, with_self: bool
):
    extra_elseif = ""
    if is_else_if:
        extra_elseif = "el"

    extra_self = ""
    if with_self:
        extra_self = "self."

    print_if_statement_header(s, statement, extra_elseif, extra_self)

    s.inc_indent()

    for member in statement.members:
        print_size_inner(s, member, with_self)

    s.dec_indent()  # if

    for elseif in statement.else_if_statements:
        print_size_if_statement(s, elseif, True, with_self)

    if len(statement.else_members) != 0:
        s.wln("else:")
        s.inc_indent()

        for m in statement.else_members:
            print_size_inner(s, m, with_self)

        s.dec_indent()
