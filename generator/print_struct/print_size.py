import model
from print_struct.util import integer_type_to_size, type_to_python_str
from writer import Writer


def print_size(s: Writer, container: model.Container):
    match container.object_type:
        case model.ObjectTypeStruct():
            pass
        case _:
            if container.manual_size_subtraction is None:
                return

    s.wln("def _size(self):")
    s.inc_indent()

    s.wln("size = 0")
    s.newline()

    for m in container.members:
        print_size_inner(s, m)

    if container.manual_size_subtraction is not None:
        s.wln(f"return size - {container.manual_size_subtraction}")
    else:
        s.wln("return size")

    s.dec_indent()
    s.newline()


def print_size_inner(s: Writer, m: model.StructMember):
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
                        raise Exception("Not constant sized struct in size")
                case model.DataTypeIPAddress():
                    s.wln("size += 4")
                case model.DataTypeString():
                    s.wln(f"size += len(self.{d.name})")
                case model.DataTypeCstring():
                    s.wln(f"size += len(self.{d.name}) + 1")
                case model.DataTypeArray(content=array):
                    s.wln(f"for i in self.{d.name}:")
                    s.inc_indent()

                    match array.inner_type:
                        case model.ArrayTypeStruct():
                            s.wln("size += i._size()")
                        case model.ArrayTypeInteger(inner_type=integer_type):
                            size = integer_type_to_size(integer_type)
                            s.wln(f"size += {size}")
                        case v:
                            raise Exception(f"{v}")

                    s.dec_indent()

                case v:
                    raise Exception(f"{v}")

        case model.StructMemberIfStatement(struct_member_content=statement):
            print_size_if_statement(s, statement)
        case model.StructMemberOptional():
            raise Exception("unimpl")
        case v:
            raise Exception(f"{v}")

    s.newline()


def print_size_if_statement(s: Writer, statement: model.StructMemberIfStatement):
    original_type = type_to_python_str(statement.original_type)
    match statement.conditional.equations:
        case model.ConditionalEquationsEquals(
            _tag, model.ConditionalEquationsEqualsValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"if self.{statement.conditional.variable_name} == {original_type}.{value[0]}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsBitwiseAnd(
            values=model.ConditionalEquationsBitwiseAndValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"if {original_type}.{value[0]} in self.{statement.conditional.variable_name}:"
                )
            else:
                raise Exception("unimpl")
        case model.ConditionalEquationsNotEquals():
            raise Exception("unimpl")

    s.inc_indent()

    for member in statement.members:
        print_size_inner(s, member)

    s.dec_indent()
