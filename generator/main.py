import cProfile
import json
import os.path
import pstats
import typing

import model
from login_utils import print_login_utils
from print_enum import print_enum, print_flag
from print_struct import print_struct
from print_struct.util import all_members_from_container
from print_update_mask import print_update_mask
from util import (
    world_version_matches,
    should_print_container,
    world_version_to_module_name,
    login_version_to_module_name,
    first_login_version,
    login_version_matches,
)
from world_utils import print_world_utils
from writer import Writer

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOGIN_MESSAGE_DIR = f"{THIS_FILE_PATH}/../wow_login_messages/wow_login_messages"
WORLD_MESSAGE_DIR = f"{THIS_FILE_PATH}/../wow_world_messages/wow_world_messages"

IR_FILE_PATH = f"{THIS_FILE_PATH}/intermediate_representation.json"

LOGIN_UTIL_FILE = f"{LOGIN_MESSAGE_DIR}/util.py"
LOGIN_OPCODES_FILE = f"{LOGIN_MESSAGE_DIR}/opcodes.py"

VANILLA = model.WorldVersion(major=1, minor=12, patch=1, build=5875)

VERSIONS = [VANILLA]


def print_includes(s: Writer, world: bool):
    s.wln("import asyncio")
    s.wln("import dataclasses")
    s.wln("import enum")
    s.wln("import struct")
    s.wln("import typing")

    if world:
        s.wln("import wow_srp")
        s.wln("from .util import packed_guid_size")
        s.wln("from .util import packed_guid_write")
        s.wln("from .util import read_packed_guid")

        s.wln("from .util import read_sized_cstring")
        s.wln("from .util import read_bool")
    else:
        s.wln("from .util import read_string")

    s.wln("from .util import read_int")
    s.wln("from .util import read_cstring")
    s.wln("from .util import read_float")

    s.newline()


def print_login_opcodes(s: Writer, opcodes: typing.Dict[str, int]):
    opcodes = dict(sorted(opcodes.items()))

    for opcode, value in opcodes.items():
        s.wln(f"{opcode}_opcode = 0x{value:02X}")

    s.newline()


def main():
    f = open(IR_FILE_PATH)
    data = json.load(f)
    m = model.IntermediateRepresentationSchema.from_json_data(data)
    m = sanitize_model(m)

    opcodes = Writer()
    print_login_opcodes(opcodes, m.login_version_opcodes)

    print_login(m.login, 0)
    for v in m.distinct_login_versions_other_than_all:
        print_login(m.login, v)

    for v in VERSIONS:
        if v == VANILLA:
            print_world(m.world, m.vanilla_update_mask, v)
        else:
            raise Exception("invalid update mask version")

    with open(LOGIN_OPCODES_FILE, "w") as f:
        f.write(opcodes.inner())


def sanitize_model(
        m: model.IntermediateRepresentationSchema,
) -> model.IntermediateRepresentationSchema:
    def containers(container: model.Container) -> model.Container:
        for d in all_members_from_container(e):
            if d.name == "class":
                d.name = "class_type"

        return container

    for e in m.world.structs.value:
        e = containers(e)

    for e in m.world.messages.value:
        e = containers(e)

    return m


def print_world(m: model.WorldObjects, update_mask: list[model.UpdateMask], v: model.WorldVersion):
    all_types = Writer()
    all_types.open("__all__ = [")

    all_types.wln('"read_client_opcodes_unencrypted",')
    all_types.wln('"read_client_opcodes_encrypted",')
    all_types.wln('"read_server_opcodes_unencrypted",')
    all_types.wln('"read_server_opcodes_encrypted",')
    all_types.wln('"expect_client_opcode_unencrypted",')
    all_types.wln('"expect_client_opcode_encrypted",')
    all_types.wln('"expect_server_opcode_unencrypted",')
    all_types.wln('"expect_server_opcode_encrypted",')

    s = Writer()

    print_update_mask(s, update_mask)

    for e in m.enums.value:
        if not world_version_matches(e.tags, v):
            continue

        print_enum(s, e)

        all_types.wln(f'"{e.name}",')

    for e in m.flags.value:
        if not world_version_matches(e.tags, v):
            continue

        print_flag(s, e)

        all_types.wln(f'"{e.name}",')

    for e in m.structs.value:
        if not should_print_container(e, v):
            continue

        print_struct(s, e)

        all_types.wln(f'"{e.name}",')

    for e in m.messages.value:
        if not should_print_container(e, v):
            continue

        print_struct(s, e)

        all_types.wln(f'"{e.name}",')

    all_types.close("]")
    all_types.double_newline()

    includes = Writer()
    print_includes(includes, world=True)

    all_types.prepend(includes)

    s.prepend(all_types)

    print_world_utils(s, m.messages.value, v)

    file_path = f"{WORLD_MESSAGE_DIR}/{world_version_to_module_name(v)}.py"
    with open(file_path, "w") as f:
        f.write(s.inner())


def print_login(m: model.LoginObjects, v: int):
    all_types = Writer()
    all_types.wln("__all__ = [")
    all_types.inc_indent()

    includes = Writer()
    print_includes(includes, world=False)

    s = Writer()
    for e in m.enums.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_enum(s, e)
        else:
            includes.wln(f"from .{login_version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.flags.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_flag(s, e)
        else:
            includes.wln(f"from .{login_version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.structs.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_struct(s, e)
        else:
            includes.wln(f"from .{login_version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.messages.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_struct(s, e)
        else:
            includes.wln(f"from .{login_version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    includes.newline()
    includes.newline()

    all_types.wln("]")
    all_types.dec_indent()
    all_types.newline()
    all_types.prepend(includes)

    s.prepend(all_types)

    print_login_utils(s, m.messages.value, v)

    file_path = f"{LOGIN_MESSAGE_DIR}/{login_version_to_module_name(v)}.py"
    with open(file_path, "w") as f:
        f.write(s.inner())


if __name__ == "__main__":
    cProfile.run("main()", sort=pstats.SortKey.CUMULATIVE)
