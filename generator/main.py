import cProfile
import json
import os.path
import pstats
import typing

import model
from generator.print_aura_mask import print_aura_mask
from generator.print_named_guid import print_named_guid
from generator.print_variable_item_random_property import print_variable_item_random_property
from login_utils import print_login_utils
from print_enum import print_enum, print_flag
from print_monster_move_spline import print_monster_move_spline
from print_struct import print_struct
from print_struct.print_tests import print_login_tests, print_world_tests
from print_struct.util import all_members_from_container
from print_update_mask import print_update_mask
from util import (
    world_version_matches,
    should_print_container,
    world_version_to_module_name,
    login_version_to_module_name,
    first_login_version,
    login_version_matches, world_version_to_title_name, VERSIONS, VANILLA, WRATH, TBC, world_version_is_wrath,
    world_version_is_tbc, world_version_is_vanilla,
)
from world_utils import print_world_utils
from writer import Writer

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOGIN_PROJECT_DIR = f"{THIS_FILE_PATH}/../wow_login_messages"
LOGIN_MESSAGE_DIR = f"{LOGIN_PROJECT_DIR}/wow_login_messages"
WORLD_PROJECT_DIR = f"{THIS_FILE_PATH}/../wow_world_messages"
WORLD_MESSAGE_DIR = f"{WORLD_PROJECT_DIR}/wow_world_messages"

IR_FILE_PATH = f"{THIS_FILE_PATH}/intermediate_representation.json"

LOGIN_UTIL_FILE = f"{LOGIN_MESSAGE_DIR}/util.py"


def print_includes(s: Writer, world: typing.Optional[model.WorldVersion]):
    s.wln("from __future__ import annotations")
    s.wln("import asyncio")
    s.wln("import dataclasses")
    s.wln("import enum")
    s.wln("import struct")
    s.wln("import typing")
    if world is not None:
        s.wln("import zlib")
    s.newline()

    if world is not None:
        s.wln("import wow_srp")
        s.wln("from .util import packed_guid_size")
        s.wln("from .util import packed_guid_write")
        s.wln("from .util import read_packed_guid")

        s.wln("from .util import read_sized_cstring")
    else:
        s.wln("from .util import read_string")

    s.wln("from .util import read_bool")
    s.wln("from .util import read_int")
    s.wln("from .util import read_cstring")
    s.wln("from .util import read_float")

    s.newline()


def main():
    f = open(IR_FILE_PATH)
    data = json.load(f)
    m = model.IntermediateRepresentationSchema.from_json_data(data)
    m = sanitize_model(m)

    print_login(m.login, 0)
    for v in m.distinct_login_versions_other_than_all:
        print_login(m.login, v)

    for v in VERSIONS:
        if v == VANILLA:
            print_world(m.world, m.vanilla_update_mask, v)
        elif v == TBC:
            print_world(m.world, m.tbc_update_mask, v)
        elif v == WRATH:
            print_world(m.world, m.wrath_update_mask, v)
        else:
            raise Exception(f"invalid update mask version {v}")


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

    if world_version_is_tbc(v) or world_version_is_wrath(v):
        print_named_guid(s)
        all_types.wln('"NamedGuid",')

        print_variable_item_random_property(s)
        all_types.wln('"VariableItemRandomProperty",')
    elif world_version_is_vanilla(v):
        # Vanilla doesn't have an Aura type
        print_aura_mask(s, v)

    all_types.wln('"AuraMask",')

    print_update_mask(s, update_mask)
    all_types.wln('"UpdateMask",')

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

        if e.name == "Vector3d":
            print_monster_move_spline(s)
            all_types.wln('"MonsterMoveSpline",')
        elif e.name == "Aura":
            # Vanilla doesn't have an Aura type
            print_aura_mask(s, v)

    for e in m.messages.value:
        if not should_print_container(e, v):
            continue

        print_struct(s, e)

        all_types.wln(f'"{e.name}",')

    all_types.close("]")
    all_types.double_newline()

    includes = Writer()
    print_includes(includes, v)

    all_types.prepend(includes)

    s.prepend(all_types)

    print_world_utils(s, m.messages.value, v)

    file_path = f"{WORLD_MESSAGE_DIR}/{world_version_to_module_name(v)}.py"
    with open(file_path, "w") as f:
        f.write(s.inner())

    tests = Writer()
    print_world_tests(tests, m)
    file_path = f"{WORLD_PROJECT_DIR}/test_world.py"
    with open(file_path, "w") as f:
        f.write(tests.inner())


def print_login(m: model.LoginObjects, v: int):
    all_types = Writer()
    all_types.wln("__all__ = [")
    all_types.inc_indent()

    includes = Writer()
    print_includes(includes, world=None)

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

    tests = Writer()
    print_login_tests(tests, m)
    file_path = f"{LOGIN_PROJECT_DIR}/test_login.py"
    with open(file_path, "w") as f:
        f.write(tests.inner())


if __name__ == "__main__":
    cProfile.run("main()", sort=pstats.SortKey.CUMULATIVE)
