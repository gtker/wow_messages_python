import model
from print_struct.util import container_should_have_size_function, all_members_from_container
from util import login_version_to_module_name, first_login_version, VERSIONS, world_version_to_module_name, \
    should_print_container, container_is_unencrypted, write_null_header_crypto
from writer import Writer


def print_tests_for_login_message(s: Writer, e: model.Container, i: int):
    s.open(f"class {e.name}{i}(unittest.IsolatedAsyncioTestCase):")

    for i, test_case in enumerate(e.tests):
        s.open(f"async def test{i}(self):")
        s.wln("reader = asyncio.StreamReader()")
        s.newline()

        s.w("data = bytes([")
        for b in test_case.raw_bytes:
            s.w_no_indent(f"{b}, ")

        s.wln_no_indent("])")
        s.newline()

        s.wln("reader.feed_data(data)")
        s.wln("reader.feed_eof()")
        s.newline()

        version = login_version_to_module_name(first_login_version(e.tags))

        version = f"wow_login_messages.{version}"
        match e.object_type:
            case model.ObjectTypeClogin():
                s.wln(f"r = await {version}.expect_client_opcode(reader, {version}.{e.name})")
            case model.ObjectTypeSlogin():
                s.wln(f"r = await {version}.expect_server_opcode(reader, {version}.{e.name})")
            case v:
                raise Exception(f"{v}")

        s.wln("self.assertIsNotNone(r)")
        s.wln("self.assertTrue(reader.at_eof())")
        if container_should_have_size_function(e):
            negative = 1  # opcode
            if e.manual_size_subtraction is not None:
                negative += e.manual_size_subtraction
            s.wln(f"self.assertEqual(len(data) - {negative}, r.size())")

        s.wln("written = bytearray(len(data))")
        s.wln("r.write(written)")
        s.wln("self.assertEqual(data, written)")

        s.close()  # async def test
        s.newline()

    s.close()  # class
    s.newline()


def print_login_tests(s: Writer, m: model.LoginObjects):
    s.wln("import asyncio")
    s.wln("import unittest")
    s.newline()
    versions = {}

    for e in m.messages:
        version = first_login_version(e.tags)
        versions[login_version_to_module_name(version)] = ""

    for v in versions:
        s.wln(f"import wow_login_messages.{v}")

    s.double_newline()

    for i, e in enumerate(m.messages):
        if len(e.tests) != 0:
            print_tests_for_login_message(s, e, i)


def print_tests_for_world_message(s: Writer, e: model.Container, version: str):
    any_fields_are_compressed = e.tags.compressed
    for d in all_members_from_container(e):
        match d.data_type:
            case model.DataTypeArray(compressed=compressed):
                if compressed:
                    any_fields_are_compressed = True

    s.open(f"class {e.name}_{version}(unittest.IsolatedAsyncioTestCase):")

    for i, test_case in enumerate(e.tests):
        s.open(f"async def test{i}(self):")
        s.wln("reader = asyncio.StreamReader()")
        s.newline()

        s.w("data = bytes([")
        for b in test_case.raw_bytes:
            s.w_no_indent(f"{b}, ")

        s.wln_no_indent("])")
        s.newline()

        s.wln("reader.feed_data(data)")
        s.wln("reader.feed_eof()")
        s.newline()

        side = ""
        header_length = 0

        match e.object_type:
            case model.ObjectTypeCmsg():
                side = "client"
                s.wln(f"r = await {version}.expect_client_opcode_unencrypted(reader, {version}.{e.name})")
                header_length = 6
            case model.ObjectTypeSmsg():
                side = "server"
                s.wln(f"r = await {version}.expect_server_opcode_unencrypted(reader, {version}.{e.name})")
                header_length = 4
            case v:
                raise Exception(f"{v}")

        s.wln("self.assertIsNotNone(r)")
        s.wln("self.assertTrue(reader.at_eof())")
        if container_should_have_size_function(e) and not any_fields_are_compressed:
            negative = 0

            match e.object_type:
                case model.ObjectTypeCmsg():
                    negative = 6
                case model.ObjectTypeSmsg():
                    negative = 4
                case _:
                    raise Exception("invalid object type for size")

            s.wln(f"self.assertEqual(len(data) - {negative}, r.size())")

        if any_fields_are_compressed:
            s.wln(f"written = bytearray(r.size() + {header_length})")
        else:
            s.wln("written = bytearray(len(data))")

        if container_is_unencrypted(e.name):
            s.wln("r.write_unencrypted(written)")
        else:
            assert side != ""
            s.wln(f"r.write_encrypted_{side}(written, NullHeaderCrypto())")

        if not any_fields_are_compressed:
            s.wln("self.assertEqual(data, written)")

        s.close()  # async def test
        s.newline()

    s.close()  # class
    s.newline()


def print_world_tests(s: Writer, m: model.WorldObjects):
    s.wln("import asyncio")
    s.wln("import unittest")
    s.wln("import struct")
    s.newline()

    for v in VERSIONS:
        version = world_version_to_module_name(v)
        s.wln(f"import wow_world_messages.{version} as {version}")

    s.double_newline()

    write_null_header_crypto(s)

    for v in VERSIONS:
        for i, e in enumerate(m.messages):
            if not should_print_container(e, v):
                continue

            if len(e.tests) != 0:
                version = world_version_to_module_name(v)
                print_tests_for_world_message(s, e, version)
