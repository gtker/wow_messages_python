import typing

import model
from writer import Writer


def container_should_have_size_function(container: model.Container):
    match container.object_type:
        case model.ObjectTypeCmsg() | model.ObjectTypeSmsg() | model.ObjectTypeMsg() | model.ObjectTypeStruct():
            if container.sizes.constant_sized:
                return False
        case _:
            if container.manual_size_subtraction is None:
                return False

    return True


def integer_type_to_size(ty: model.IntegerType) -> int:
    match ty:
        case model.IntegerType.I16:
            return 2
        case model.IntegerType.I32:
            return 4
        case model.IntegerType.I64:
            return 8
        case model.IntegerType.I8:
            return 1
        case model.IntegerType.U16:
            return 2
        case model.IntegerType.U32:
            return 4
        case model.IntegerType.U48:
            return 5
        case model.IntegerType.U64:
            return 8
        case model.IntegerType.U8:
            return 1


def type_to_wowm_str(ty: model.DataType) -> str:
    match ty:
        case model.DataTypeInteger(content=integer_type):
            text = f"{integer_type}".replace("IntegerType.", "").lower()
            return text

        case model.DataTypeBool(content=integer_type):
            size = integer_type_to_size(integer_type)
            return f"Bool{size * 8}"

        case model.DataTypeCstring():
            return "CString"

        case model.DataTypeSizedCstring():
            return "SizedCString"

        case model.DataTypeString():
            return "String"
        case model.DataTypeFloatingPoint():
            return "f32"

        case model.DataTypeStruct(
            content=model.DataTypeStructContent(struct_data=e)
        ):
            return e.name

        case model.DataTypeEnum(content=model.DataTypeEnumContent(type_name=type_name)):
            return type_name

        case model.DataTypeFlag(content=model.DataTypeFlagContent(type_name=type_name)):
            return type_name

        case model.DataTypeArray(content=model.Array(inner_type=inner_type, size=size)):
            inner_type = array_type_to_wowm_str(inner_type)
            size = array_size_to_wowm_str(size)

            return f"{inner_type}[{size}]"

        case model.DataTypeGold():
            return "Gold"
        case model.DataTypeGUID():
            return "Guid"
        case model.DataTypeIPAddress():
            return "IpAddress"
        case model.DataTypeLevel():
            return "Level"
        case model.DataTypeLevel16():
            return "Level16"
        case model.DataTypeLevel32():
            return "Level32"
        case model.DataTypeSpell():
            return "Spell"
        case model.DataTypeSpell16():
            return "Spell16"
        case model.DataTypeItem():
            return "Item"
        case model.DataTypeMilliseconds():
            return "Milliseconds"
        case model.DataTypePackedGUID():
            return "PackedGuid"
        case model.DataTypeSeconds():
            return "Seconds"
        case model.DataTypePopulation():
            return "Population"
        case model.DataTypeDateTime():
            return "DateTime"
        case model.DataTypeUpdateMask():
            return "UpdateMask"

        case model.DataTypeAchievementDoneArray():
            return "AchievementDoneArray"
        case model.DataTypeAchievementInProgressArray():
            return "AchievementInProgressArray"
        case model.DataTypeAddonArray():
            return "AddonArray"
        case model.DataTypeAuraMask():
            return "AuraMask"

        case model.DataTypeEnchantMask():
            return "EnchantMask"
        case model.DataTypeInspectTalentGearMask():
            return "InspectTalentGearMask"
        case model.DataTypeMonsterMoveSpline():
            return "MonsterMoveSpline"
        case model.DataTypeNamedGUID():
            return "NamedGuid"
        case model.DataTypeVariableItemRandomProperty():
            return "VariableItemRandomProperty"
        case model.DataTypeCacheMask():
            return "CacheMask"
        case v:
            raise Exception(f"{v}")


def array_size_to_wowm_str(size: model.ArraySize):
    match size:
        case model.ArraySizeFixed(size=size):
            return size
        case model.ArraySizeVariable(size=size):
            return size
        case model.ArraySizeEndless():
            return "-"

        case v:
            raise Exception(f"{v}")


def array_type_to_wowm_str(ty: model.ArrayType):
    match ty:
        case model.ArrayTypeCstring():
            return "CString"
        case model.ArrayTypeGUID():
            return "Guid"
        case model.ArrayTypeInteger(content=integer_type):
            text = f"{integer_type}".replace("IntegerType.", "").lower()
            return text
        case model.ArrayTypeSpell():
            return "Spell"
        case model.ArrayTypePackedGUID():
            return "PackedGuid"
        case model.ArrayTypeStruct(content=model.ArrayTypeStructContent(struct_data=e)):
            return e.name
        case v:
            raise Exception(f"{v}")


def type_to_python_str(ty: model.DataType) -> str:
    match ty:
        case model.DataTypeInteger():
            return "int"
        case model.DataTypeBool():
            return "bool"

        case model.DataTypeString() | model.DataTypeCstring() | model.DataTypeSizedCstring():
            return "str"
        case model.DataTypeFloatingPoint():
            return "float"
        case model.DataTypeStruct(
            content=model.DataTypeStructContent(struct_data=e)
        ):
            return e.name
        case model.DataTypeEnum(content=model.DataTypeEnumContent(type_name=type_name)):
            return type_name
        case model.DataTypeFlag(content=model.DataTypeFlagContent(type_name=type_name)):
            return type_name

        case model.DataTypeArray(content=model.Array(inner_type=inner_type)):
            inner_type = array_type_to_python_str(inner_type)
            return f"typing.List[{inner_type}]"

        case model.DataTypeGold():
            return "int"
        case model.DataTypeGUID():
            return "int"
        case model.DataTypeIPAddress():
            return "int"
        case model.DataTypeLevel():
            return "int"
        case model.DataTypeLevel16():
            return "int"
        case model.DataTypeLevel32():
            return "int"
        case model.DataTypeSpell():
            return "int"
        case model.DataTypeSpell16():
            return "int"
        case model.DataTypeItem():
            return "int"
        case model.DataTypeMilliseconds():
            return "int"
        case model.DataTypePackedGUID():
            return "int"
        case model.DataTypeSeconds():
            return "int"
        case model.DataTypePopulation():
            return "float"
        case model.DataTypeDateTime():
            return "int"
        case model.DataTypeUpdateMask():
            return "UpdateMask"

        case model.DataTypeAchievementDoneArray():
            return "AchievementDoneArray"
        case model.DataTypeAchievementInProgressArray():
            return "AchievementInProgressArray"
        case model.DataTypeAddonArray():
            return "AddonArray"
        case model.DataTypeAuraMask():
            return "AuraMask"

        case model.DataTypeEnchantMask():
            return "EnchantMask"
        case model.DataTypeInspectTalentGearMask():
            return "InspectTalentGearMask"
        case model.DataTypeMonsterMoveSpline():
            return "MonsterMoveSpline"
        case model.DataTypeNamedGUID():
            return "NamedGUID"
        case model.DataTypeVariableItemRandomProperty():
            return "VariableItemRandomProperty"
        case model.DataTypeCacheMask():
            return "CacheMask"
        case v:
            raise Exception(f"{v}")


def array_type_to_python_str(ty: model.ArrayType):
    match ty:
        case model.ArrayTypeCstring():
            return "str"
        case model.ArrayTypeGUID():
            return "int"
        case model.ArrayTypeInteger():
            return "int"
        case model.ArrayTypeSpell():
            return "int"
        case model.ArrayTypePackedGUID():
            return "int"
        case model.ArrayTypeStruct(content=model.ArrayTypeStructContent(struct_data=e)):
            return e.name
        case v:
            raise Exception(f"{v}")


def all_members_from_container(
        container: model.Container,
) -> typing.List[model.Definition]:
    out_members = []

    def inner(m: model.StructMember, out_members: typing.List[model.Definition]):
        def inner_if(
                statement: model.IfStatement, out_members: typing.List[model.Definition]
        ):
            for member in statement.members:
                inner(member, out_members)

            for elseif in statement.else_if_statements:
                inner_if(elseif, out_members)

            for member in statement.else_members:
                inner(member, out_members)

        match m:
            case model.StructMemberDefinition(_tag, definition):
                out_members.append(definition)

            case model.StructMemberIfStatement(_tag, struct_member_content=statement):
                inner_if(statement, out_members)

            case model.StructMemberOptional(
                _tag, model.OptionalMembers(members=members)
            ):
                for member in members:
                    inner(member, out_members)

            case v:
                raise Exception(f"invalid struct member {v}")

    for m in container.members:
        inner(m, out_members)

    return out_members


def print_optional_statement_header(s: Writer, optional: model.OptionalMembers):
    s.wln(f"# {optional.name}: optional")
    s.w("if")
    i = 0

    extra_self = "self."

    for m in optional.members:
        match m:
            case model.StructMemberDefinition(struct_member_content=d):
                if d.constant_value is not None \
                        or d.size_of_fields_before_size is not None \
                        or d.used_as_size_in is not None:
                    continue

                if i != 0:
                    s.w_no_indent(" and")

                s.w_no_indent(f" {extra_self}{d.name} is not None")

        i += 1

    s.wln_no_indent(":")
    s.inc_indent()


def print_if_statement_header(
        s: Writer,
        statement: model.IfStatement,
        extra_elseif: str,
        extra_self: str,
):
    original_type = type_to_python_str(statement.original_type)
    var_name = statement.conditional.variable_name

    match statement.conditional.equations:
        case model.ConditionalEquationsEquals(
            _tag, model.ConditionalEquationsEqualsValues(value=value)
        ):
            if len(value) == 1:
                s.wln(
                    f"{extra_elseif}if {extra_self}{var_name} == {original_type}.{value[0]}:"
                )
            else:
                s.w(f"{extra_elseif}if {extra_self}{var_name} in {{")
                for i, val in enumerate(value):
                    if i != 0:
                        s.w_no_indent(", ")
                    s.w_no_indent(f"{original_type}.{val}")
                s.wln_no_indent("}:")

        case model.ConditionalEquationsBitwiseAnd(
            values=model.ConditionalEquationsBitwiseAndValues(value=value)
        ):
            s.w(f"{extra_elseif}if ")
            for i, val in enumerate(value):
                if i != 0:
                    s.w_no_indent(" or ")
                s.w_no_indent(f"{original_type}.{val} in {extra_self}{var_name}")
            s.wln_no_indent(":")

        case model.ConditionalEquationsNotEquals(values=values):
            s.wln(
                f"{extra_elseif}if {extra_self}{var_name} != {original_type}.{values.value}:"
            )
