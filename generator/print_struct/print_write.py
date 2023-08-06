import typing

import model
from model import Container
from print_struct.util import print_if_statement_header, type_to_wowm_str, print_optional_statement_header
from util import container_is_unencrypted
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


def addable_write_values(
        d: model.Definition,
) -> typing.Optional[typing.Tuple[str, str]]:
    match d.data_type:
        case model.DataTypeInteger(content=integer_type):
            if d.used_as_size_in is not None:
                return integer_type_to_struct_pack(integer_type), f"len(self.{d.used_as_size_in})"
            elif d.size_of_fields_before_size is not None:
                return integer_type_to_struct_pack(integer_type), "self.size()"
            elif d.constant_value is not None:
                return integer_type_to_struct_pack(integer_type), str(d.constant_value.value)
            else:
                return integer_type_to_struct_pack(integer_type), f"self.{d.name}"

        case model.DataTypeBool(content=integer_type):
            return integer_type_to_struct_pack(integer_type), f"self.{d.name}"

        case model.DataTypeFlag(
            content=model.DataTypeFlagContent(integer_type=integer_type)
        ):
            return integer_type_to_struct_pack(integer_type), f"self.{d.name}.value"

        case model.DataTypeEnum(
            content=model.DataTypeEnumContent(integer_type=integer_type)
        ):
            return integer_type_to_struct_pack(integer_type), f"self.{d.name}.value"

        case model.DataTypeDateTime() \
             | model.DataTypeGold() \
             | model.DataTypeSeconds() \
             | model.DataTypeMilliseconds() \
             | model.DataTypeIPAddress():
            return "I", f"self.{d.name}"

        case model.DataTypePopulation():
            return "f", f"self.{d.name}"

        case model.DataTypeString():
            return f"B{{len(self.{d.name})}}s", f"len(self.{d.name}), self.{d.name}.encode('utf-8')"

        case model.DataTypeCstring():
            return f"{{len(self.{d.name})}}sB", f"self.{d.name}.encode('utf-8'), 0"

        case model.DataTypeSizedCstring():
            return f"I{{len(self.{d.name})}}sB", f"len(self.{d.name}) + 1, self.{d.name}.encode('utf-8'), 0"

        case model.DataTypeGUID():
            return "Q", f"self.{d.name}"

        case model.DataTypeLevel():
            return "B", f"self.{d.name}"

        case model.DataTypeLevel16():
            return "H", f"self.{d.name}"

        case model.DataTypeLevel32():
            return "I", f"self.{d.name}"

        case model.DataTypeFloatingPoint():
            return "f", f"self.{d.name}"

        case model.DataTypeArray(content=array):
            if array.compressed:
                return None

            match array.inner_type:
                case model.ArrayTypeInteger(content=inner_type):
                    ty = integer_type_to_struct_pack(inner_type)
                    return f"{{len(self.{d.name})}}{ty}", f"*self.{d.name}"

                case model.ArrayTypeGUID():
                    return f"{{len(self.{d.name})}}Q", f"*self.{d.name}"

                case model.ArrayTypePackedGUID() | model.ArrayTypeCstring() | model.ArrayTypeStruct():
                    return None

        case model.DataTypeUpdateMask() \
             | model.DataTypeAuraMask() \
             | model.DataTypeMonsterMoveSpline() \
             | model.DataTypePackedGUID() \
             | model.DataTypeStruct():
            return None

        case v:
            print(v)
            raise Exception(f"{v}")


def print_write_struct_member(s: Writer, d: model.Definition, prefix: str):
    s.wln(f"# {d.name}: {type_to_wowm_str(d.data_type)}")
    addable = addable_write_values(d)
    if addable is not None:
        fmt, data = addable
        extra_format = ""
        if "{" in fmt:
            extra_format = "f"
        s.wln(f"{prefix}fmt += {extra_format}'{fmt}'")
        if "," in data or "*" in data:
            s.wln(f"{prefix}data.extend([{data}])")
        else:
            s.wln(f"{prefix}data.append({data})")
    else:
        match d.data_type:
            case model.DataTypeArray(content=array):
                match array:
                    case model.Array(inner_type=inner_type):
                        if array.compressed:
                            s.wln(f"_{d.name}_fmt = ''")
                            s.wln(f"_{d.name}_data = []")
                            s.newline()

                            s.wln(f"_{d.name}_decompressed_size = 0")
                            s.open(f"if len(self.{d.name}) != 0:")

                            print_array_write_inner(s, d, inner_type, f"_{d.name}_", "self.")

                            s.wln(f"_{d.name}_bytes = struct.pack(_{d.name}_fmt, *_{d.name}_data)")
                            s.wln(f"_{d.name}_decompressed_size = len(_{d.name}_bytes)")
                            s.wln(f"_{d.name}_bytes = list(_{d.name}_bytes)")
                            s.newline()

                            s.wln("_fmt += 'I'")
                            s.wln(f"_data.append(_{d.name}_decompressed_size)")
                            s.newline()

                            s.wln(f"_fmt += f'{{len(_{d.name}_bytes)}}B'")

                            s.wln(f"_data.extend(list(_{d.name}_bytes))")
                            s.close()  # if len( != 0

                            s.open("else:")
                            s.wln("_fmt += 'I'")
                            s.wln(f"_data.append(_{d.name}_decompressed_size)")
                            s.newline()

                            s.close()  # else:

                        else:
                            print_array_write_inner(s, d, inner_type, prefix, "self.")

                    case v:
                        raise Exception(f"{v}")

            case model.DataTypeStruct(content=model.DataTypeStructContent()):
                s.wln(f"{prefix}fmt, {prefix}data = self.{d.name}.write({prefix}fmt, {prefix}data)")

            case model.DataTypePackedGUID():
                s.wln(f"{prefix}fmt, {prefix}data = packed_guid_write(self.{d.name}, {prefix}fmt, {prefix}data)")

            case model.DataTypeUpdateMask() | model.DataTypeAuraMask() | model.DataTypeMonsterMoveSpline():
                s.wln(f"{prefix}fmt, {prefix}data = self.{d.name}.write({prefix}fmt, {prefix}data)")

            case v:
                print(v)
                raise Exception(f"{v}")

    s.newline()


def print_array_write_inner(s: Writer, d: model.Definition, inner_type: model.DataType, prefix: str, extra_self: str):
    match inner_type:
        case model.ArrayTypeInteger(content=inner_type):
            ty = integer_type_to_struct_pack(inner_type)
            s.wln(f"{prefix}fmt += f'{{len({extra_self}{d.name})}}{ty}'")
            s.wln(f"{prefix}data.extend({extra_self}{d.name})")

        case model.ArrayTypeStruct():
            s.wln(f"for i in {extra_self}{d.name}:")
            s.inc_indent()
            s.wln(f"{prefix}fmt, {prefix}data = i.write({prefix}fmt, {prefix}data)")
            s.dec_indent()  # for i in

        case model.ArrayTypeCstring():
            s.wln(f"for i in {extra_self}{d.name}:")
            s.inc_indent()
            s.wln(f"{prefix}fmt += f'{{len(i)}}sB'")
            s.wln(f"{prefix}data.append(i.encode('utf-8'))")
            s.wln(f"{prefix}data.append(0)")
            s.dec_indent()  # for i in

        case model.ArrayTypeGUID():
            s.wln(f"{prefix}fmt += f'len({{{extra_self}{d.name}}})Q'")
            s.wln(f"{prefix}data.extend({extra_self}{d.name})")

        case model.ArrayTypePackedGUID():
            s.wln(f"for i in {extra_self}{d.name}:")
            s.inc_indent()
            s.wln(f"{prefix}fmt, {prefix}data = packed_guid_write(i, {prefix}fmt, {prefix}data)")
            s.dec_indent()  # for i in

        case v:
            raise Exception(f"{v}")


def get_write_and_remaining_members(
        members: list[model.StructMember]
) -> (str, str, list[model.StructMember]):
    fmt = ""
    data = ""

    for i, m in enumerate(members):
        match m:
            case model.StructMemberDefinition(struct_member_content=d):
                addable = addable_write_values(d)
                if addable is not None:
                    addable_fmt, addable_data = addable
                    fmt += addable_fmt
                    if len(data) != 0:
                        data += f", {addable_data}"
                    else:
                        data += addable_data
                else:
                    return fmt, data, members[i:]

            case model.StructMemberIfStatement() | model.StructMemberOptional():
                return fmt, data, members[i:]
            case v:
                raise Exception(f"{v}")

    return fmt, data, []


def print_write(s: Writer, container: Container, object_type: model.ObjectType):
    unencrypted = container_is_unencrypted(container.name)

    writer = "writer: typing.Union[asyncio.StreamWriter, bytearray]"
    match object_type:
        case model.ObjectTypeStruct():
            s.wln("def write(self, _fmt, _data):")
        case model.ObjectTypeCmsg() | model.ObjectTypeSmsg():
            if unencrypted:
                s.wln(f"def write_unencrypted(self, {writer}):")
            else:
                version_string = "vanilla"
                match object_type:
                    case model.ObjectTypeCmsg():
                        s.wln("def write_encrypted_client(")
                    case model.ObjectTypeSmsg():
                        s.wln("def write_encrypted_server(")
                    case _:
                        raise Exception("unknown object_type")
                s.inc_indent()
                s.wln("self,")
                s.wln(f"{writer},")
                s.wln(f"header_crypto: wow_srp.{version_string}_header.HeaderCrypto,")
                s.dec_indent()
                s.wln("):")
        case _:
            s.wln(f"def write(self, {writer}):")
    s.inc_indent()

    match object_type:
        case model.ObjectTypeStruct():
            pass
        case model.ObjectTypeClogin(opcode=opcode) | model.ObjectTypeSlogin(
            opcode=opcode
        ):
            s.wln("_fmt = '<B' # opcode")
            s.wln(f"_data = [{opcode}]")
            s.newline()

        case model.ObjectTypeCmsg(opcode=opcode) | model.ObjectTypeSmsg(opcode=opcode):
            opcode_size = 0
            match object_type:
                case model.ObjectTypeCmsg(opcode=opcode):
                    opcode_size = 4
                case model.ObjectTypeSmsg(opcode=opcode):
                    opcode_size = 2
                case v:
                    raise Exception(f"{v}")

            size = "self.size()"
            if container.sizes.constant_sized:
                size = str(container.sizes.maximum_size)

            if not unencrypted:
                s.wln(
                    f"_data = bytes(header_crypto.encrypt_server_header({size} + {opcode_size}, 0x{opcode:04X}))"
                )
            else:
                s.wln(f"_data = bytearray({opcode_size + 2})")
                s.wln(f'struct.pack_into(">H", _data, 0, {size} + {opcode_size})')
                if opcode_size == 4:
                    s.wln(f'struct.pack_into("<I", _data, 2, 0x{opcode:04X})')
                elif opcode_size == 2:
                    s.wln(f'struct.pack_into("<H", _data, 2, 0x{opcode:04X})')
                else:
                    raise Exception("invalid opcode size")

            s.wln(f'_fmt = "<{opcode_size + 2}s"')
            s.wln("_data = [_data]")
            s.newline()

            if container.tags.compressed:
                s.wln('_compressed_fmt = "<"')
                s.wln("_compressed_data = []")
                s.newline()

        case _:
            raise Exception("unsupported write header")

    prefix = "_"
    if container.tags.compressed:
        prefix = "_compressed_"

    print_write_members_addable(s, container.members, prefix)

    match object_type:
        case model.ObjectTypeStruct():
            s.wln("return _fmt, _data")
        case model.ObjectTypeClogin() \
             | model.ObjectTypeSlogin() \
             | model.ObjectTypeCmsg() \
             | model.ObjectTypeSmsg():
            if container.tags.compressed:
                s.wln("_uncompressed_data = struct.pack(_compressed_fmt, *_compressed_data)")
                s.wln("_compressed_data = zlib.compress(_uncompressed_data)")
                s.newline()

                s.wln("_fmt += 'I'")
                s.wln("_data.append(len(_uncompressed_data))")
                s.newline()

                s.wln("_fmt += f'{len(_compressed_data)}s'")
                s.wln("_data.append(_compressed_data)")
                s.newline()

            s.wln("_data = struct.pack(_fmt, *_data)")

            s.open("if isinstance(writer, bytearray):")

            s.open("for i in range(0, len(_data)):")
            s.wln("writer[i] = _data[i]")
            s.close()
            s.wln("return")

            s.close()

            s.wln("writer.write(_data)")
        case _:
            raise Exception("unsupported write header")

    s.dec_indent()  # def write
    s.newline()


def print_write_members_addable(s: Writer, members: list[model.StructMember], prefix: str):
    fmt, data, extra_members = get_write_and_remaining_members(members)
    if len(members) != 0:
        if len(fmt) != 0:
            extra_format = ""
            if "{" in fmt:
                extra_format = "f"
            s.wln(f"_fmt += {extra_format}'{fmt}'")
            if "," in data or "*" in data:
                s.wln(f"_data.extend([{data}])")
            else:
                s.wln(f"_data.append({data})")

        for m in extra_members:
            print_write_member(s, m, prefix)


def print_write_member(s: Writer, m: model.StructMember, prefix: str):
    match m:
        case model.StructMemberDefinition(_tag, definition):
            print_write_struct_member(s, definition, prefix)

        case model.StructMemberIfStatement(_tag, statement):
            print_write_if_statement(s, statement, False, prefix)

        case model.StructMemberOptional(_tag, struct_member_content=optional):
            print_optional_statement_header(s, optional)

            print_write_members_addable(s, optional.members, prefix)

            s.dec_indent()  # if optional

        case _:
            raise Exception("invalid struct member")


def print_write_if_statement(s: Writer,
                             statement: model.IfStatement,
                             is_else_if: bool,
                             prefix: str):
    extra_elseif = ""
    if is_else_if:
        extra_elseif = "el"

    print_if_statement_header(s, statement, extra_elseif, "self.")

    s.inc_indent()

    print_write_members_addable(s, statement.members, prefix)

    s.dec_indent()  # if

    for elseif in statement.else_if_statements:
        print_write_if_statement(s, elseif, True, prefix)

    if len(statement.else_members) != 0:
        s.wln("else:")
        s.inc_indent()

        print_write_members_addable(s, statement.else_members, prefix)

        s.dec_indent()
