import typing

import model
from writer import Writer

VANILLA = model.WorldVersion(major=1, minor=12, patch=1, build=5875)
TBC = model.WorldVersion(major=2, minor=4, patch=3, build=8606)
WRATH = model.WorldVersion(major=3, minor=3, patch=5, build=12340)

VERSIONS = [VANILLA, TBC, WRATH]


def should_print_container(container: model.Container, v: model.WorldVersion) -> bool:
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


def world_version_is_wrath(version: model.WorldVersion) -> bool:
    return version == WRATH


def world_version_is_tbc(version: model.WorldVersion) -> bool:
    return version == TBC


def world_version_is_vanilla(version: model.WorldVersion) -> bool:
    return version == VANILLA


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


def container_is_unencrypted(name: str) -> bool:
    return name == "CMSG_AUTH_SESSION" or name == "SMSG_AUTH_CHALLENGE"


def world_version_to_module_name(v: model.WorldVersion) -> str:
    match v:
        case model.WorldVersion(major=1):
            return "vanilla"
        case model.WorldVersion(major=2):
            return "tbc"
        case model.WorldVersion(major=3):
            return "wrath"
        case v:
            raise Exception(f"unknown version {v}")


def world_version_to_title_name(v: model.WorldVersion) -> str:
    return world_version_to_module_name(v).capitalize()


def login_version_to_module_name(v: int) -> str:
    if v == 0:
        return "all"
    else:
        return f"version{v}"


def first_login_version(tags: model.ObjectTags) -> int:
    match tags.version:
        case model.ObjectVersionsLogin(version_type=version_type):
            match version_type:
                case model.LoginVersionsAll():
                    return 0
                case model.LoginVersionsSpecific(versions=versions):
                    return versions[0]
                case _:
                    raise Exception("invalid login versions type")
        case _:
            raise Exception("invalid version")


def login_version_matches(tags: model.ObjectTags, value: int) -> bool:
    match tags.version:
        case model.ObjectVersionsLogin(version_type=version_type):
            match version_type:
                case model.LoginVersionsAll():
                    return True
                case model.LoginVersionsSpecific(versions=versions):
                    return value in versions
                case _:
                    raise Exception("invalid login versions type")
        case _:
            raise Exception("invalid version")


def write_null_header_crypto(s: Writer):
    s.write_block("""
class NullHeaderCrypto:
    def decrypt_server_header(self, data) -> (int, int):
        size = data[0] << 8 | data[1]
        opcode = data[2] | data[3] << 8
        return size, opcode

    def decrypt_client_header(self, data) -> (int, int):
        size = data[0] << 8 | data[1]
        opcode = data[2] | data[3] << 8 | data[4] << 16 | data[5] << 24
        return size, opcode

    def encrypt_server_header(self, size: int, opcode: int) -> bytearray:
        data = bytearray(4)
        struct.pack_into(">H", data, 0, size)
        struct.pack_into("<H", data, 2, opcode)
        return data

    def encrypt_client_header(self, size: int, opcode: int) -> bytearray:
        data = bytearray(6)
        struct.pack_into(">H", data, 0, size)
        struct.pack_into("<I", data, 2, opcode)
        return data
    """)

    s.double_newline()


def container_needs_size_in_read(container: model.Container) -> bool:
    def inner_if(statement: model.IfStatement) -> bool:
        for m in statement.members:
            if inner(m):
                return True

        for elseif in statement.else_if_statements:
            if inner_if(elseif):
                return True

        return False

    def inner(m: model.StructMember) -> bool:
        match m:
            case model.StructMemberDefinition(struct_member_content=d):
                match d.data_type:
                    case model.DataTypeArray(compressed=compressed, size=size):
                        if compressed:
                            return True

                        match size:
                            case model.ArraySizeEndless():
                                return True

            case model.StructMemberIfStatement(struct_member_content=statement):
                if inner_if(statement):
                    return True

        return False

    if container.optional is not None:
        return True

    for m in container.members:
        if inner(m):
            return True

    return False
