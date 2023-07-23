import json
import os.path
import typing

import model
from print_enum import print_enum, print_flag
from print_struct import print_struct
from writer import Writer

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOGIN_MESSAGE_DIR = f"{THIS_FILE_PATH}/../wow_login_messages/wow_login_messages"

IR_FILE_PATH = f"{THIS_FILE_PATH}/intermediate_representation.json"

LOGIN_UTIL_FILE = f"{LOGIN_MESSAGE_DIR}/util.py"
LOGIN_OPCODES_FILE = f"{LOGIN_MESSAGE_DIR}/opcodes.py"


def print_includes(s: Writer):
    s.wln("import asyncio")
    s.wln("import dataclasses")
    s.wln("import enum")
    s.wln("import struct")
    s.wln("import typing")
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

    opcodes = Writer()
    print_login_opcodes(opcodes, m.login_version_opcodes)

    print_login(m.login, 0)
    for v in m.distinct_login_versions_other_than_all:
        print_login(m.login, v)

    with open(LOGIN_OPCODES_FILE, "w") as f:
        f.write(opcodes.inner())


def print_login(m: model.LoginObjects, v: int):
    includes = Writer()

    all_types = Writer()
    all_types.wln("__all__ = [")
    all_types.inc_indent()

    print_includes(includes)

    s = Writer()
    for e in m.enums.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_enum(s, e)
        else:
            includes.wln(f"from {version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.flags.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_flag(s, e)
        else:
            includes.wln(f"from {version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.structs.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_struct(s, e)
        else:
            includes.wln(f"from {version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    for e in m.messages.value:
        if not login_version_matches(e.tags, v):
            continue

        first = first_login_version(e.tags)
        if first == v:
            print_struct(s, e)
        else:
            includes.wln(f"from {version_to_module_name(first)} import {e.name}")

        all_types.wln(f'"{e.name}",')

    includes.newline()
    includes.newline()

    all_types.wln("]")
    all_types.dec_indent()
    all_types.newline()
    all_types.prepend(includes)

    s.prepend(all_types)

    file_path = f"{LOGIN_MESSAGE_DIR}/{version_to_module_name(v)}.py"
    with open(file_path, "w") as f:
        f.write(s.inner())


def version_to_module_name(v: int) -> str:
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


if __name__ == "__main__":
    main()
