import typing

import model
from writer import Writer


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
            content=model.DataTypeStructContent(type_name=type_name)
        ):
            return type_name
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
        case v:
            raise Exception("{v}")


def array_type_to_python_str(ty: model.ArrayType):
    match ty:
        case model.ArrayTypeCstring():
            return "str"
        case model.ArrayTypeGUID():
            return "int"
        case model.ArrayTypeInteger():
            return "int"
        case model.ArrayTypePackedGUID():
            return "int"
        case model.ArrayTypeStruct(content=content):
            return content.type_name


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


def print_if_statement_header(
        s: Writer, statement: model.IfStatement, extra_elseif: str, extra_self: str
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
