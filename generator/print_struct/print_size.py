import typing

import model
from print_struct.print_write import print_array_write_inner, print_write_member
from print_struct.util import (
    integer_type_to_size,
    print_if_statement_header, type_to_wowm_str, container_should_have_size_function, print_optional_statement_header,
)
from writer import Writer


def print_size(s: Writer, container: model.Container):
    if not container_should_have_size_function(container):
        return

    s.open("def size(self) -> int:")

    if container.tags.compressed:
        print_size_for_compressed_container(s, container)
    else:
        print_size_until_inner_members(s, container.members, container.manual_size_subtraction, True)

    s.dec_indent()
    s.newline()


def print_size_until_inner_members(s: Writer, members: list[model.StructMember],
                                   manual_size_subtraction: typing.Optional[int], return_early: bool):
    count, strings, uncounted_members = get_size_and_remaining_members(members)

    if manual_size_subtraction is not None:
        count -= manual_size_subtraction

    size = str(count)
    if len(strings) != 0:
        size += f" + {' + '.join(strings)}"

    if len(uncounted_members) == 0 and return_early:
        s.wln(f"return {size}")
    else:
        if not return_early:
            s.wln(f"_size += {size}")
        else:
            s.wln(f"_size = {size}")

        if len(uncounted_members) != 0:
            s.newline()

        for m in uncounted_members:
            print_size_inner(s, m)

        if return_early:
            s.wln(f"return _size")


def print_size_for_compressed_container(s, container):
    s.wln("_fmt = ''")
    s.wln("_data = []")
    s.newline()
    for m in container.members:
        print_write_member(s, m, "_")
    s.wln("_uncompressed_data = struct.pack(_fmt, *_data)")
    s.wln("_compressed_data = zlib.compress(_uncompressed_data)")
    s.wln("return len(_compressed_data) + 4")


def array_size_inner_values(
        array: model.DataTypeArray, name: str, extra_self: str
) -> typing.Union[str, int]:
    size = 0
    match array.inner_type:
        case model.ArrayTypeGUID():
            size = 8
        case model.ArrayTypeStruct(struct_data=e):
            if e.sizes.constant_sized:
                size = e.sizes.maximum_size
            else:
                return f"sum([i.size() for i in {extra_self}{name}])"
        case model.ArrayTypePackedGUID():
            return f"sum([packed_guid_size(i) for i in {extra_self}{name}])"
        case model.ArrayTypeCstring():
            return f"sum([len(i) + 1 for i in {extra_self}{name}])"
        case model.ArrayTypeInteger(integer_type=integer_type):
            size = integer_type_to_size(integer_type)
        case model.ArrayTypeSpell():
            size = 4
        case v:
            raise Exception(f"{v}")

    match array.size:
        case model.ArraySizeFixed(size=array_size):
            return size * int(array_size)
        case model.ArraySizeVariable() | model.ArraySizeEndless():
            return f"{size} * len({extra_self}{name})"
        case v2:
            raise Exception(f"{v2}")


def addable_size_value(
        data_type: model.DataType, extra_self: str, name: str
) -> typing.Optional[typing.Tuple[int, typing.Optional[str]]]:
    match data_type:
        case model.DataTypeStruct(struct_data=e):
            if not e.sizes.constant_sized:
                return 0, f"{extra_self}{name}.size()"
            else:
                return e.sizes.maximum_size, None
        case model.DataTypeString() | model.DataTypeCstring():
            return 1, f"len({extra_self}{name})"
        case model.DataTypeSizedCstring():
            return 5, f"len({extra_self}{name})"
        case model.DataTypePackedGUID():
            return 0, f"packed_guid_size({extra_self}{name})"
        case model.DataTypeAchievementDoneArray() | model.DataTypeAchievementInProgressArray() | model.DataTypeAddonArray() | model.DataTypeCacheMask() | model.DataTypeVariableItemRandomProperty() | model.DataTypeInspectTalentGearMask() | model.DataTypeNamedGUID() | model.DataTypeEnchantMask() | model.DataTypeUpdateMask() | model.DataTypeAuraMask() | model.DataTypeMonsterMoveSpline():
            return 0, f"{extra_self}{name}.size()"
        case model.DataTypeArray(compressed=compressed):
            if compressed:
                return None
            size = array_size_inner_values(data_type, name, extra_self)
            if isinstance(size, str):
                return 0, size
            elif isinstance(size, int):
                return size, None
        case model.DataTypeInteger(integer_type=integer_type):
            return integer_type_to_size(integer_type), None
        case model.DataTypeBool(integer_type=integer_type):
            return integer_type_to_size(integer_type), None
        case model.DataTypeEnum(integer_type=integer_type):
            return integer_type_to_size(integer_type), None
        case model.DataTypeFlag(integer_type=integer_type):
            return integer_type_to_size(integer_type), None

        case model.DataTypeSpell() | model.DataTypeItem() | model.DataTypeDateTime() \
             | model.DataTypeGold() \
             | model.DataTypeSeconds() \
             | model.DataTypeMilliseconds() \
             | model.DataTypeIPAddress():
            return 4, None
        case model.DataTypePopulation():
            return 4, None
        case model.DataTypeGUID():
            return 8, None
        case model.DataTypeLevel():
            return 1, None
        case model.DataTypeLevel16() | model.DataTypeSpell16():
            return 2, None
        case model.DataTypeLevel32():
            return 4, None
        case model.DataTypeFloatingPoint():
            return 4, None

        case v:
            raise Exception(f"unhandled ty {v}")

    return None


def get_size_and_remaining_members(members: list[model.StructMember]) -> typing.Tuple[
    int, list[str], list[model.StructMember]]:
    count = 0
    strings = []
    uncounted_members: typing.List[model.StructMember] = []

    for m in members:
        match m:
            case model.StructMemberDefinition(struct_member_content=d):
                addable = addable_size_value(d.data_type, "self.", d.name)
                if addable is not None:
                    addable_count, addable_string = addable
                    count += addable_count
                    if addable_string is not None:
                        strings.append(addable_string)
                else:
                    uncounted_members.append(m)
            case model.StructMemberIfStatement() | model.StructMemberOptional():
                uncounted_members.append(m)
            case v:
                raise Exception(f"{v}")

    return count, strings, uncounted_members


def print_size_inner(s: Writer, m: model.StructMember):
    extra_self = "self."

    match m:
        case model.StructMemberDefinition(struct_member_content=d):
            s.wln(f"# {d.name}: {type_to_wowm_str(d.data_type)}")

            match d.data_type:
                case model.DataTypeArray(compressed=compressed, inner_type=inner_type):
                    if compressed:
                        s.wln(f"_{d.name}_fmt = ''")
                        s.wln(f"_{d.name}_data = []")
                        s.newline()

                        s.open(f"if len({extra_self}{d.name}) != 0:")

                        print_array_write_inner(s, d, inner_type, f"_{d.name}_", extra_self)

                        s.wln(f"_{d.name}_bytes = struct.pack(_{d.name}_fmt, *_{d.name}_data)")
                        s.wln(f"_size += len(_{d.name}_bytes) + 4")
                        s.close()

                        s.open("else:")
                        s.wln("_size += 4")
                        s.close()  # else:

                    else:
                        raise Exception("uncompressed array?")
                case v:
                    raise Exception(f"{v}")

        case model.StructMemberIfStatement(struct_member_content=statement):
            print_size_if_statement(s, statement, False)
        case model.StructMemberOptional(struct_member_content=optional):
            print_optional_statement_header(s, optional)

            print_size_until_inner_members(s, optional.members, None, False)

            s.close()  # if optional

        case v:
            raise Exception(f"{v}")

    s.newline()


def print_size_if_statement(s: Writer, statement: model.IfStatement, is_else_if: bool):
    extra_elseif = ""
    if is_else_if:
        extra_elseif = "el"

    extra_self = "self."

    print_if_statement_header(s, statement, extra_elseif, extra_self)

    s.inc_indent()

    print_size_until_inner_members(s, statement.members, None, False)

    s.dec_indent()  # if

    for elseif in statement.else_if_statements:
        print_size_if_statement(s, elseif, True)
