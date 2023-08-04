import typing

import model

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


def should_print_container(container: model.Container, v: model.WorldVersion) -> bool:
    if container.name not in WORLD_ALLOWED_OBJECTS:
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

