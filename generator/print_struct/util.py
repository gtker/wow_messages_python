import typing

import model


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
        case model.DataTypeString() | model.DataTypeCstring():
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

        case model.DataTypeAchievementDoneArray():
            return "AchievementDoneArray"
        case model.DataTypeAchievementInProgressArray():
            return "AchievementInProgressArray"
        case model.DataTypeAddonArray():
            return "AddonArray"
        case model.DataTypeAuraMask():
            return "AuraMask"

        case model.DataTypeDateTime():
            return "DateTime"
        case model.DataTypeEnchantMask():
            return "EnchantMask"
        case model.DataTypeGold():
            return "Gold"
        case model.DataTypeGUID():
            return "GUID"
        case model.DataTypeInspectTalentGearMask():
            return "InspectTalentGearMask"
        case model.DataTypeIPAddress():
            return "int"
        case model.DataTypeLevel():
            return "Level"
        case model.DataTypeLevel16():
            return "Level16"
        case model.DataTypeLevel32():
            return "Level32"
        case model.DataTypeMilliseconds():
            return "Milliseconds"
        case model.DataTypeMonsterMoveSpline():
            return "MonsterMoveSpline"
        case model.DataTypeNamedGUID():
            return "NamedGUID"
        case model.DataTypePackedGUID():
            return "PackedGUID"
        case model.DataTypeSeconds():
            return "Seconds"
        case model.DataTypeSizedCstring():
            return "SizedCString"
        case model.DataTypeUpdateMask():
            return "UpdateMask"
        case model.DataTypeVariableItemRandomProperty():
            return "VariableItemRandomProperty"
        case model.DataTypePopulation():
            return "float"
        case v:
            raise Exception("{v}")


def array_type_to_python_str(ty: model.ArrayType):
    match ty:
        case model.ArrayTypeCstring():
            return "str"
        case model.ArrayTypeGUID():
            return "GUID"
        case model.ArrayTypeInteger():
            return "int"
        case model.ArrayTypePackedGUID():
            return "PackedGUID"
        case model.ArrayTypeStruct(inner_type=inner_type):
            return inner_type


def all_members_from_container(
    container: model.Container,
) -> typing.List[model.Definition]:
    out_members = []

    def inner(m: model.StructMember, out_members: typing.List[model.Definition]):
        match m:
            case model.StructMemberDefinition(_tag, definition):
                out_members.append(definition)

            case model.StructMemberIfStatement(
                _tag, model.IfStatement(members=members)
            ):
                for member in members:
                    inner(member, out_members)

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
