import typing

import model
from print_struct.util import all_members_from_container

WORLD_ALLOWED_OBJECTS = [
    "CMSG_AUTH_SESSION",
    "CMSG_CHAR_ENUM",
    "CMSG_PLAYER_LOGIN",
    "Character",
    "CharacterGear",
    "SMSG_AUTH_CHALLENGE",
    "SMSG_AUTH_RESPONSE",
    "SMSG_CHAR_ENUM",
    "Vector2d",
    "Vector3d",
]


def should_print_container_if(statement: model.IfStatement) -> bool:
    match statement.conditional.equations:
        case model.ConditionalEquationsEquals(
            _tag, model.ConditionalEquationsEqualsValues(value=value)
        ):
            if len(value) != 1:
                return False

        case model.ConditionalEquationsBitwiseAnd(
            values=model.ConditionalEquationsBitwiseAndValues(value=value)
        ):
            if len(value) != 1:
                return False

        case model.ConditionalEquationsNotEquals(values=values):
            pass

        case _:
            raise Exception("invalid case")

    for m in statement.members:
        if not should_print_container_struct_member(m):
            return False

    for elseif in statement.else_if_statements:
        if not should_print_container_if(elseif):
            return False

    for m in statement.else_members:
        if not should_print_container_struct_member(m):
            return False

    return True


def should_print_container_struct_member(m: model.StructMember) -> bool:
    match m:
        case model.StructMemberDefinition(struct_member_content=content):
            forbidden_types = [
                "TransportInfo",
                "SpellCastTargets",
                "MovementInfo",
                "Mail",
                "Object",
            ]

            match content.data_type:
                case model.DataTypeStruct(content=content):
                    if content.type_name in forbidden_types:
                        return False
                case model.DataTypeArray(content=array):
                    match array.inner_type:
                        case model.ArrayTypeStruct(content=content):
                            if content.type_name in forbidden_types:
                                return False

        case model.StructMemberIfStatement(struct_member_content=statement):
            if not should_print_container_if(statement):
                return False
        case model.StructMemberOptional(struct_member_content=optional):
            return False
        case _:
            raise Exception("unknown m")

    return True


def should_print_container(container: model.Container, v: model.WorldVersion) -> bool:
    if container.name == "CMSG_AUTH_SESSION":
        return True

    if container.tags.compressed is not None:
        return False

    match container.object_type:
        case model.ObjectTypeMsg():
            return False
        case _:
            pass

    for d in all_members_from_container(container):
        match d.data_type:
            case model.DataTypeAchievementDoneArray() | model.DataTypeAchievementInProgressArray() | model.DataTypeAddonArray() | model.DataTypeAuraMask() | model.DataTypeEnchantMask() | model.DataTypeInspectTalentGearMask() | model.DataTypeMonsterMoveSpline() | model.DataTypeNamedGUID() | model.DataTypeUpdateMask() | model.DataTypeVariableItemRandomProperty() | model.DataTypePackedGUID() | model.DataTypeSizedCstring():
                return False
            case model.DataTypeArray(content=array):
                match array.size:
                    case model.ArraySizeEndless():
                        return False

    for m in container.members:
        if not should_print_container_struct_member(m):
            return False

    if not world_version_matches(container.tags, v):
        return False

    return True


def world_version_satisfies(t: model.WorldVersion, o: model.WorldVersion) -> bool:
    """
    Version `t` is fully satisfied by version `o`.
    """
    if t.major != o.major:
        return False
    # Major versions are equal

    def test(t: typing.Optional[int], o: typing.Optional[int]):
        if t is None and o is None:
            return True
        # Either t or o are not None

        # t is more general than o
        if t is None and o is not None:
            return False

        # t is less general than o
        if t is not None and o is None:
            return True

        if t != o:
            return False

        return None

    minor = test(t.minor, o.minor)
    if minor is not None:
        return minor

    patch = test(t.patch, o.patch)
    if patch is not None:
        return patch

    build = test(t.build, o.build)
    if build is not None:
        return build

    return True


def world_version_matches(tags: model.ObjectTags, version: model.WorldVersion) -> bool:
    match tags.version:
        case model.ObjectVersionsLogin(version_type=version_type):
            raise Exception("invalid version")
        case model.ObjectVersionsWorld(version_type=version_type):
            match version_type:
                case model.WorldVersionsAll():
                    return True
                case model.WorldVersionsSpecific(versions=versions):
                    for v in versions:
                        if world_version_satisfies(version, v):
                            return True
                case _:
                    raise Exception("invalid world versions type")

    return False


def world_version_to_module_name(v: model.WorldVersion) -> str:
    match v:
        case model.WorldVersion(major=1):
            return "vanilla"
        case _:
            raise Exception("unknown version")
