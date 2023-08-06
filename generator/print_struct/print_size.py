import model
from print_struct.util import integer_type_to_size, type_to_python_str
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

    s.wln("size = 0")
    s.newline()

    for m in container.members:
        print_size_inner(s, m, True)

    if container.manual_size_subtraction is not None:
        s.wln(f"return size - {container.manual_size_subtraction}")
    else:
        s.wln("return size")

    s.dec_indent()
    s.newline()


def print_size_inner(s: Writer, m: model.StructMember, with_self: bool):
    extra_self = ""
    if with_self:
        extra_self = "self."

    match m:
        case model.StructMemberDefinition(struct_member_content=d):
            s.wln(f"# {d.name}: {d.data_type}")
            match d.data_type:
                case model.DataTypeInteger(content=integer_type):
                    size = integer_type_to_size(integer_type)
                    s.wln(f"size += {size}")
                case model.DataTypeBool(content=integer_type):
                    size = integer_type_to_size(integer_type)
                    s.wln(f"size += {size}")
                case model.DataTypeEnum(content=content):
                    size = integer_type_to_size(content.integer_type)
                    s.wln(f"size += {size}")
                case model.DataTypeFlag(content=content):
                    size = integer_type_to_size(content.integer_type)
                    s.wln(f"size += {size}")
                case model.DataTypeStruct(content=content):
                    if content.sizes.constant_sized:
                        size = content.sizes.maximum_size
                        s.wln(f"size += {size}")
                    else:
                        s.wln(f"size += {extra_self}{d.name}._size()")
                case model.DataTypeDateTime() | model.DataTypeGold() | model.DataTypeSeconds() | model.DataTypeMilliseconds() | model.DataTypeIPAddress():
                    s.wln("size += 4")
                case model.DataTypePopulation():
                    s.wln("size += 4")
                case model.DataTypeString():
                    s.wln(f"size += len({extra_self}{d.name})")
                case model.DataTypeCstring():
                    s.wln(f"size += len({extra_self}{d.name}) + 1")
                case model.DataTypeGUID():
                    s.wln(f"size += 8")
                case model.DataTypeLevel():
                    s.wln(f"size += 1")
                case model.DataTypeLevel16():
                    s.wln(f"size += 2")
                case model.DataTypeLevel32():
                    s.wln(f"size += 4")

                case model.DataTypeFloatingPoint():
                    s.wln("size += 4")

                case model.DataTypePackedGUID():
                    s.wln(f"{d.name}_byte_mask = 0")

                    s.wln("for i in range(0, 8):")
                    s.inc_indent()

                    s.wln(f"if {extra_self}{d.name} & (1 << i * 8):")
                    s.inc_indent()

                    s.wln(f"{d.name}_byte_mask |= 1 << i")

                    s.wln(f"size += 1 + bin({d.name}_byte_mask)[2:].count('1')")

                    s.dec_indent()
                    s.dec_indent()

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
                            case model.ArrayTypeInteger(content=integer_type):
                                size = integer_type_to_size(integer_type)
                                s.wln(f"size += {size}")
                            case model.ArrayTypeCstring():
                                s.wln("size += len(i) + 1")
                            case model.ArrayTypeGUID():
                                s.wln("size += 8")
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

    original_type = type_to_python_str(statement.original_type)
    match statement.conditional.equations:
        case model.ConditionalEquationsEquals(
            _tag, model.ConditionalEquationsEqualsValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"{extra_elseif}if {extra_self}{statement.conditional.variable_name} == {original_type}.{value[0]}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsBitwiseAnd(
            values=model.ConditionalEquationsBitwiseAndValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"{extra_elseif}if {extra_self}{original_type}.{value[0]} in {extra_self}{statement.conditional.variable_name}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsNotEquals(values=values):
            s.wln(
                f"if {extra_self}{original_type}.{values.value} not in {extra_self}{statement.conditional.variable_name}:"
            )

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
