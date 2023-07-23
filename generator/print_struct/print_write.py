import model
from model import Container
from print_struct.util import type_to_python_str
from writer import Writer


def integer_type_to_struct_pack(ty: model.IntegerType):
    match ty:
        case model.IntegerType.U8:
            return "B"
        case model.IntegerType.I8:
            return "b"
        case model.IntegerType.U16:
            return "H"
        case model.IntegerType.I16:
            return "h"
        case model.IntegerType.U32:
            return "I"
        case model.IntegerType.I32:
            return "i"
        case model.IntegerType.U64:
            return "Q"
        case model.IntegerType.I64:
            return "q"
        case model.IntegerType.U48:
            return "IH"


def print_write_struct_member(s: Writer, d: model.Definition):
    s.wln(f"# {d.name}: {d.data_type}")
    match d.data_type:
        case model.DataTypeInteger(content=integer_type):
            if d.used_as_size_in is not None:
                s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
                s.wln(f"data.append(len(self.{d.used_as_size_in}))")

            elif d.size_of_fields_before_size is not None:
                s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
                s.wln("data.append(self._size())")
            elif d.constant_value is not None:
                s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
                s.wln(f"data.append({int(d.constant_value.value)})")
            else:
                s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
                s.wln(f"data.append(self.{d.name})")

        case model.DataTypeBool(content=integer_type):
            s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
            s.wln(f"data.append(self.{d.name})")

        case model.DataTypeFlag(
            content=model.DataTypeFlagContent(integer_type=integer_type)
        ):
            s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
            s.wln(f"data.append(self.{d.name}.value)")

        case model.DataTypeEnum(
            content=model.DataTypeEnumContent(integer_type=integer_type)
        ):
            s.wln(f"fmt += '{integer_type_to_struct_pack(integer_type)}'")
            s.wln(f"data.append(self.{d.name}.value)")

        case model.DataTypeIPAddress():
            s.wln("fmt += 'I'")
            s.wln(f"data.append(self.{d.name})")

        case model.DataTypePopulation():
            s.wln("fmt += 'f'")
            s.wln(f"data.append(self.{d.name})")

        case model.DataTypeString():
            s.wln(f"fmt += f'B{{len(self.{d.name})}}s'")
            s.wln(f"data.append(len(self.{d.name}))")
            s.wln(f"data.append(self.{d.name}.encode('utf-8'))")

        case model.DataTypeCstring():
            s.wln(f"fmt += f'{{len(self.{d.name})}}sB'")
            s.wln(f"data.append(self.{d.name}.encode('utf-8'))")
            s.wln("data.append(0)")

        case model.DataTypeArray(content=content):
            match content:
                case model.Array(inner_type=inner_type):
                    match inner_type:
                        case model.ArrayTypeInteger(inner_type=inner_type):
                            ty = integer_type_to_struct_pack(inner_type)
                            s.wln(f"fmt += f'{{len(self.{d.name})}}{ty}'")
                            s.wln(f"data.extend(self.{d.name})")

                        case model.ArrayTypeStruct():
                            s.wln(f"for i in self.{d.name}:")
                            s.inc_indent()
                            s.wln("fmt, data = i.write(fmt, data)")
                            s.dec_indent()  # for i in

                        case v:
                            raise Exception(f"{v}")

                case v:
                    raise Exception(f"{v}")

        case model.DataTypeStruct(content=model.DataTypeStructContent()):
            s.wln(f"fmt, data = self.{d.name}.write(fmt, data)")

        case v:
            print(v)
            raise Exception(f"{v}")

    s.newline()


def print_write(s: Writer, container: Container):
    match container.object_type:
        case model.ObjectTypeStruct():
            s.wln("def write(self, fmt, data):")
        case _:
            s.wln("def write(self, writer: asyncio.StreamWriter):")
    s.inc_indent()

    match container.object_type:
        case model.ObjectTypeStruct():
            pass
        case model.ObjectTypeClogin(opcode=opcode) | model.ObjectTypeSlogin(
            opcode=opcode
        ):
            s.wln("fmt = '<B' # opcode")
            s.wln(f"data = [{opcode}]")
            s.newline()
        case _:
            raise Exception("unsupported write header")

    for m in container.members:
        print_write_member(s, m)

    match container.object_type:
        case model.ObjectTypeStruct():
            s.wln("return fmt, data")
        case model.ObjectTypeClogin() | model.ObjectTypeSlogin():
            s.wln("data = struct.pack(fmt, *data)")
            s.wln("writer.write(data)")
        case _:
            raise Exception("unsupported write header")

    s.dec_indent()  # def write
    s.newline()


def print_write_member(s: Writer, m: model.StructMember):
    match m:
        case model.StructMemberDefinition(_tag, definition):
            print_write_struct_member(s, definition)

        case model.StructMemberIfStatement(_tag, statement):
            print_write_if_statement(s, statement)

        case model.StructMemberOptional(_tag, model.OptionalMembers(members=members)):
            raise Exception("optional unimpl")

        case _:
            raise Exception("invalid struct member")


def print_write_if_statement(s: Writer, statement: model.IfStatement):
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
        case v:
            raise Exception(f"{v}")

    s.inc_indent()

    for member in statement.members:
        print_write_member(s, member)

    s.dec_indent()  # if
