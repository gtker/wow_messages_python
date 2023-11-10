import asyncio
import unittest
import struct

import wow_world_messages.vanilla as vanilla
import wow_world_messages.tbc as tbc


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



class CMSG_WORLD_TELEPORT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 28, 8, 0, 0, 0, 239, 190, 173, 222, 1, 0, 0, 0, 0, 0, 128, 63, 0, 0, 0, 64, 0, 0, 64, 64, 0, 0, 128, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_WORLD_TELEPORT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 28, 8, 0, 0, 0, 154, 61, 9, 2, 213, 1, 0, 0, 0, 0, 226, 67, 0, 176, 201, 69, 0, 128, 30, 69, 219, 15, 73, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_WORLD_TELEPORT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_TELEPORT_TO_UNIT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 11, 9, 0, 0, 0, 86, 117, 114, 116, 110, 101, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_TELEPORT_TO_UNIT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_CREATE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 22, 54, 0, 0, 0, 68, 101, 97, 100, 98, 101, 101, 102, 0, 1, 1, 1, 8, 0, 14, 2, 4, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CHAR_CREATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_ENUM_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 55, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CHAR_ENUM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_DELETE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 56, 0, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CHAR_DELETE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CHAR_CREATE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 58, 0, 47, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHAR_CREATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CHAR_ENUM_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 59, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHAR_ENUM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CHAR_DELETE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 60, 0, 57, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHAR_DELETE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PLAYER_LOGIN_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 61, 0, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_PLAYER_LOGIN)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_NEW_WORLD_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 22, 62, 0, 1, 0, 0, 0, 0, 160, 186, 68, 0, 236, 137, 197, 205, 204, 184, 65, 205, 204, 76, 62, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_NEW_WORLD)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_TRANSFER_PENDING_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 63, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_TRANSFER_PENDING)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CHARACTER_LOGIN_FAILED_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 65, 0, 65, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHARACTER_LOGIN_FAILED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGIN_SETTIMESPEED_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 66, 0, 10, 50, 115, 22, 137, 136, 136, 60, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_LOGIN_SETTIMESPEED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PLAYER_LOGOUT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 74, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_PLAYER_LOGOUT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_LOGOUT_REQUEST_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 75, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_LOGOUT_REQUEST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGOUT_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 7, 76, 0, 0, 0, 0, 0, 1, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_LOGOUT_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGOUT_COMPLETE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 2, 77, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_LOGOUT_COMPLETE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_NAME_QUERY_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 28, 81, 0, 239, 190, 173, 222, 0, 0, 0, 0, 65, 115, 100, 102, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_NAME_QUERY_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 29, 81, 0, 239, 190, 173, 222, 0, 0, 0, 0, 65, 115, 100, 102, 0, 65, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_NAME_QUERY_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PET_NAME_QUERY_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 16, 82, 0, 0, 0, 239, 190, 173, 222, 239, 190, 173, 222, 222, 202, 250, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_PET_NAME_QUERY)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_PET_NAME_QUERY_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 17, 83, 0, 239, 190, 173, 222, 65, 66, 67, 68, 69, 70, 0, 222, 202, 250, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_PET_NAME_QUERY_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ITEM_QUERY_SINGLE_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 224, 88, 0, 62, 28, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0, 83, 109, 105, 116, 101, 39, 115, 32, 77, 105, 103, 104, 116, 121, 32, 72, 97, 109, 109, 101, 114, 0, 0, 0, 0, 154, 76, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 155, 60, 0, 0, 31, 12, 0, 0, 17, 0, 0, 0, 223, 5, 0, 0, 255, 1, 0, 0, 23, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 11, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92, 66, 0, 0, 166, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 172, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ITEM_QUERY_SINGLE_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CREATURE_QUERY_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 46, 97, 0, 69, 0, 0, 0, 84, 104, 105, 110, 103, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CREATURE_QUERY_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_IGNORE_LIST_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 11, 107, 0, 1, 239, 190, 173, 222, 254, 15, 220, 186, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_IGNORE_LIST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 19, 107, 0, 2, 239, 190, 173, 222, 254, 15, 220, 186, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_IGNORE_LIST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_MESSAGECHAT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 35, 149, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 84, 104, 105, 115, 32, 105, 115, 32, 97, 32, 115, 97, 121, 32, 109, 101, 115, 115, 97, 103, 101, 46, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_MESSAGECHAT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_MESSAGECHAT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 51, 150, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 84, 104, 105, 115, 32, 105, 115, 32, 97, 32, 115, 97, 121, 32, 109, 101, 115, 115, 97, 103, 101, 46, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_MESSAGECHAT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_JOIN_CHANNEL_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 29, 151, 0, 0, 0, 71, 101, 110, 101, 114, 97, 108, 32, 45, 32, 69, 108, 119, 121, 110, 110, 32, 70, 111, 114, 101, 115, 116, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_JOIN_CHANNEL)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 34, 151, 0, 0, 0, 76, 111, 99, 97, 108, 68, 101, 102, 101, 110, 115, 101, 32, 45, 32, 69, 108, 119, 121, 110, 110, 32, 70, 111, 114, 101, 115, 116, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_JOIN_CHANNEL)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_UPDATE_OBJECT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 97, 169, 0, 1, 0, 0, 0, 0, 3, 1, 4, 4, 49, 0, 0, 0, 0, 0, 0, 0, 0, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 63, 0, 0, 224, 64, 0, 0, 144, 64, 0, 0, 0, 0, 0, 0, 0, 0, 219, 15, 73, 64, 1, 0, 0, 0, 2, 7, 0, 64, 0, 16, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 100, 0, 0, 0, 1, 1, 1, 1, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_UPDATE_OBJECT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 133, 169, 0, 1, 0, 0, 0, 0, 3, 1, 4, 4, 49, 0, 0, 0, 0, 0, 0, 0, 0, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 63, 0, 0, 224, 64, 0, 0, 144, 64, 0, 0, 0, 0, 0, 0, 0, 0, 219, 15, 73, 64, 1, 0, 0, 0, 5, 23, 0, 64, 16, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 128, 63, 100, 0, 0, 0, 100, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 50, 0, 0, 0, 50, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_UPDATE_OBJECT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_DESTROY_OBJECT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 170, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_DESTROY_OBJECT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_USE_ITEM_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 9, 171, 0, 0, 0, 255, 24, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_USE_ITEM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_FORWARD_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 181, 0, 0, 0, 1, 0, 0, 0, 99, 42, 122, 1, 115, 186, 11, 198, 24, 227, 238, 194, 148, 168, 165, 66, 44, 231, 248, 62, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_FORWARD_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_FORWARD_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 181, 0, 1, 5, 1, 0, 0, 0, 99, 42, 122, 1, 115, 186, 11, 198, 24, 227, 238, 194, 148, 168, 165, 66, 44, 231, 248, 62, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_FORWARD_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_BACKWARD_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 182, 0, 0, 0, 2, 0, 0, 0, 16, 87, 91, 2, 117, 165, 11, 198, 111, 244, 244, 194, 189, 13, 165, 66, 107, 108, 146, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_BACKWARD_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_BACKWARD_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 182, 0, 1, 5, 2, 0, 0, 0, 16, 87, 91, 2, 117, 165, 11, 198, 111, 244, 244, 194, 189, 13, 165, 66, 107, 108, 146, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_BACKWARD_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 183, 0, 0, 0, 0, 0, 0, 0, 242, 49, 122, 1, 36, 203, 11, 198, 48, 32, 223, 194, 61, 23, 166, 66, 3, 81, 36, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 183, 0, 1, 5, 0, 0, 0, 0, 242, 49, 122, 1, 36, 203, 11, 198, 48, 32, 223, 194, 61, 23, 166, 66, 3, 81, 36, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_STRAFE_LEFT_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 184, 0, 0, 0, 5, 0, 0, 0, 159, 210, 121, 1, 238, 193, 11, 198, 253, 68, 8, 195, 36, 126, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_STRAFE_LEFT_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_STRAFE_LEFT_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 184, 0, 1, 5, 5, 0, 0, 0, 159, 210, 121, 1, 238, 193, 11, 198, 253, 68, 8, 195, 36, 126, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_STRAFE_LEFT_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_STRAFE_RIGHT_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 185, 0, 0, 0, 9, 0, 0, 0, 159, 210, 121, 1, 238, 193, 11, 198, 253, 68, 8, 195, 36, 126, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_STRAFE_RIGHT_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_STRAFE_RIGHT_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 185, 0, 1, 5, 9, 0, 0, 0, 159, 210, 121, 1, 238, 193, 11, 198, 253, 68, 8, 195, 36, 126, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_STRAFE_RIGHT_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_STRAFE_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 186, 0, 0, 0, 1, 0, 0, 0, 70, 211, 121, 1, 22, 192, 11, 198, 248, 49, 7, 195, 115, 127, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_STRAFE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_STRAFE_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 186, 0, 1, 5, 1, 0, 0, 0, 70, 211, 121, 1, 22, 192, 11, 198, 248, 49, 7, 195, 115, 127, 167, 66, 184, 157, 194, 62, 127, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_STRAFE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_JUMP_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 48, 187, 0, 0, 0, 1, 32, 0, 0, 32, 214, 121, 1, 27, 173, 11, 198, 157, 76, 5, 195, 209, 74, 167, 66, 184, 157, 194, 62, 0, 0, 0, 0, 216, 147, 254, 192, 77, 186, 109, 63, 159, 246, 189, 62, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_JUMP_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_JUMP_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 48, 187, 0, 1, 5, 1, 32, 0, 0, 32, 214, 121, 1, 27, 173, 11, 198, 157, 76, 5, 195, 209, 74, 167, 66, 184, 157, 194, 62, 0, 0, 0, 0, 216, 147, 254, 192, 77, 186, 109, 63, 159, 246, 189, 62, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_JUMP_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_TURN_LEFT_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 188, 0, 0, 0, 16, 0, 0, 0, 251, 190, 121, 1, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_TURN_LEFT_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_TURN_LEFT_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 188, 0, 1, 5, 16, 0, 0, 0, 251, 190, 121, 1, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_TURN_LEFT_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_TURN_RIGHT_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 189, 0, 0, 0, 32, 0, 0, 0, 251, 190, 121, 1, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_TURN_RIGHT_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_START_TURN_RIGHT_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 189, 0, 1, 5, 32, 0, 0, 0, 251, 190, 121, 1, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_START_TURN_RIGHT_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_TURN_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 190, 0, 0, 0, 0, 0, 0, 0, 151, 166, 91, 2, 37, 162, 11, 198, 57, 130, 248, 194, 222, 72, 165, 66, 16, 19, 156, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_TURN_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_STOP_TURN_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 190, 0, 1, 5, 0, 0, 0, 0, 151, 166, 91, 2, 37, 162, 11, 198, 57, 130, 248, 194, 222, 72, 165, 66, 16, 19, 156, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_STOP_TURN_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_RUN_MODE_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 194, 0, 0, 0, 1, 0, 0, 0, 65, 27, 91, 2, 85, 185, 11, 198, 248, 132, 1, 195, 173, 49, 167, 66, 46, 14, 195, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_RUN_MODE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_RUN_MODE_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 194, 0, 1, 5, 1, 0, 0, 0, 65, 27, 91, 2, 85, 185, 11, 198, 248, 132, 1, 195, 173, 49, 167, 66, 46, 14, 195, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_RUN_MODE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_WALK_MODE_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 195, 0, 0, 0, 1, 1, 0, 0, 154, 23, 91, 2, 2, 189, 11, 198, 78, 88, 1, 195, 38, 41, 167, 66, 46, 14, 195, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_WALK_MODE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_WALK_MODE_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 195, 0, 1, 5, 1, 1, 0, 0, 154, 23, 91, 2, 2, 189, 11, 198, 78, 88, 1, 195, 38, 41, 167, 66, 46, 14, 195, 64, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_WALK_MODE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_TELEPORT_ACK_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 13, 199, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_TELEPORT_ACK_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_TELEPORT_ACK_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 36, 199, 0, 1, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 135, 69, 0, 160, 37, 197, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_TELEPORT_ACK_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_FALL_LAND_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 201, 0, 0, 0, 0, 0, 0, 0, 165, 217, 121, 1, 173, 149, 11, 198, 120, 245, 2, 195, 241, 246, 165, 66, 75, 71, 175, 61, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_FALL_LAND_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_FALL_LAND_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 201, 0, 1, 5, 0, 0, 0, 0, 165, 217, 121, 1, 173, 149, 11, 198, 120, 245, 2, 195, 241, 246, 165, 66, 75, 71, 175, 61, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_FALL_LAND_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_FACING_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 218, 0, 0, 0, 1, 0, 0, 0, 94, 45, 122, 1, 151, 175, 11, 198, 66, 10, 232, 194, 227, 37, 165, 66, 167, 79, 35, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_FACING_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_SET_FACING_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 218, 0, 1, 5, 1, 0, 0, 0, 94, 45, 122, 1, 151, 175, 11, 198, 66, 10, 232, 194, 227, 37, 165, 66, 167, 79, 35, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_SET_FACING_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_FORCE_RUN_SPEED_CHANGE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 226, 0, 1, 6, 0, 0, 0, 0, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_FORCE_RUN_SPEED_CHANGE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_FORCE_RUN_SPEED_CHANGE_ACK_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 48, 227, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 23, 246, 1, 203, 171, 11, 198, 7, 134, 248, 194, 142, 209, 165, 66, 237, 153, 127, 64, 57, 3, 0, 0, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_FORCE_RUN_SPEED_CHANGE_ACK)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_HEARTBEAT_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 238, 0, 0, 0, 1, 0, 0, 0, 70, 49, 122, 1, 25, 199, 11, 198, 254, 110, 224, 194, 26, 245, 165, 66, 3, 81, 36, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_MOVE_HEARTBEAT_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_HEARTBEAT_Server_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 32, 238, 0, 1, 5, 1, 0, 0, 0, 70, 49, 122, 1, 25, 199, 11, 198, 254, 110, 224, 194, 26, 245, 165, 66, 3, 81, 36, 64, 133, 3, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.MSG_MOVE_HEARTBEAT_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_TUTORIAL_FLAGS_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 34, 253, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_TUTORIAL_FLAGS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_STANDSTATECHANGE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 1, 1, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_STANDSTATECHANGE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_TEXT_EMOTE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 20, 4, 1, 0, 0, 34, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_TEXT_EMOTE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_AUTOEQUIP_ITEM_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 10, 1, 0, 0, 255, 24, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_AUTOEQUIP_ITEM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_INITIATE_TRADE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 22, 1, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_INITIATE_TRADE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CANCEL_TRADE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 28, 1, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CANCEL_TRADE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_INITIAL_SPELLS_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 167, 42, 1, 0, 40, 0, 78, 0, 0, 0, 81, 0, 0, 0, 107, 0, 0, 0, 196, 0, 0, 0, 198, 0, 0, 0, 201, 0, 0, 0, 203, 0, 0, 0, 204, 0, 0, 0, 10, 2, 0, 0, 156, 2, 0, 0, 78, 9, 0, 0, 153, 9, 0, 0, 175, 9, 0, 0, 234, 11, 0, 0, 37, 13, 0, 0, 181, 20, 0, 0, 89, 24, 0, 0, 102, 24, 0, 0, 103, 24, 0, 0, 77, 25, 0, 0, 78, 25, 0, 0, 203, 25, 0, 0, 98, 28, 0, 0, 99, 28, 0, 0, 187, 28, 0, 0, 194, 32, 0, 0, 33, 34, 0, 0, 117, 35, 0, 0, 118, 35, 0, 0, 156, 35, 0, 0, 165, 35, 0, 0, 117, 80, 0, 0, 118, 80, 0, 0, 119, 80, 0, 0, 120, 80, 0, 0, 128, 81, 0, 0, 147, 84, 0, 0, 148, 84, 0, 0, 11, 86, 0, 0, 26, 89, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_INITIAL_SPELLS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CAST_SPELL_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 46, 1, 0, 0, 120, 80, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CAST_SPELL)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CANCEL_CAST_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 47, 1, 0, 0, 120, 80, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CANCEL_CAST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 47, 1, 0, 0, 242, 33, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CANCEL_CAST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SET_SELECTION_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 61, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_SET_SELECTION)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_ATTACKSWING_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 65, 1, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_ATTACKSWING)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ATTACKSTART_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 18, 67, 1, 23, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ATTACKSTART)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ATTACKSTOP_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 68, 1, 1, 23, 1, 100, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ATTACKSTOP)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ATTACKERSTATEUPDATE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 51, 74, 1, 128, 0, 0, 0, 1, 23, 1, 100, 57, 5, 0, 0, 1, 0, 0, 0, 0, 0, 128, 166, 68, 52, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ATTACKERSTATEUPDATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ITEM_PUSH_RESULT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 43, 102, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 255, 24, 0, 0, 0, 96, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ITEM_PUSH_RESULT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_QUERY_TIME_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 206, 1, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_QUERY_TIME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_QUERY_TIME_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 207, 1, 148, 152, 80, 97, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_QUERY_TIME_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PING_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 220, 1, 0, 0, 239, 190, 173, 222, 222, 202, 250, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_PING)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_PONG_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 221, 1, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_PONG)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SETSHEATHED_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 224, 1, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_SETSHEATHED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_AUTH_CHALLENGE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 236, 1, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_AUTH_CHALLENGE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_unencrypted(written)
        self.assertEqual(data, written)


class CMSG_AUTH_SESSION_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 172, 237, 1, 0, 0, 243, 22, 0, 0, 0, 0, 0, 0, 65, 0, 136, 2, 216, 73, 136, 157, 239, 5, 37, 187, 193, 171, 167, 138, 219, 164, 251, 163, 231, 126, 103, 172, 234, 198, 86, 1, 0, 0, 120, 156, 117, 204, 189, 14, 194, 48, 12, 4, 224, 242, 30, 188, 12, 97, 64, 149, 200, 66, 195, 140, 76, 226, 34, 11, 199, 169, 140, 203, 79, 159, 30, 22, 36, 6, 115, 235, 119, 119, 129, 105, 89, 64, 203, 105, 51, 103, 163, 38, 199, 190, 91, 213, 199, 122, 223, 125, 18, 190, 22, 192, 140, 113, 36, 228, 18, 73, 168, 194, 228, 149, 72, 10, 201, 197, 61, 216, 182, 122, 6, 75, 248, 52, 15, 21, 70, 115, 103, 187, 56, 204, 122, 199, 151, 139, 189, 220, 38, 204, 254, 48, 66, 214, 230, 202, 1, 168, 184, 144, 128, 81, 252, 183, 164, 80, 112, 184, 18, 243, 63, 38, 65, 253, 181, 55, 144, 25, 102, 143, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_AUTH_SESSION)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_unencrypted(written)


class SMSG_AUTH_RESPONSE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 238, 1, 13, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_AUTH_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 7, 238, 1, 27, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_AUTH_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 238, 1, 12, 239, 190, 173, 222, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_AUTH_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_ZONEUPDATE_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 244, 1, 0, 0, 101, 6, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_ZONEUPDATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 244, 1, 0, 0, 12, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_ZONEUPDATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_COMPRESSED_UPDATE_OBJECT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 137, 246, 1, 60, 1, 0, 0, 120, 1, 99, 97, 96, 96, 96, 100, 58, 236, 17, 120, 64, 158, 53, 8, 200, 134, 3, 191, 51, 13, 14, 140, 64, 222, 195, 39, 172, 12, 140, 242, 206, 10, 140, 30, 129, 32, 185, 3, 242, 138, 64, 18, 194, 110, 176, 63, 206, 205, 192, 160, 1, 228, 131, 20, 242, 3, 113, 10, 16, 51, 29, 47, 217, 192, 132, 110, 218, 81, 225, 147, 246, 40, 166, 1, 213, 0, 213, 66, 76, 131, 176, 113, 153, 198, 222, 130, 97, 218, 231, 154, 9, 168, 110, 3, 170, 129, 155, 6, 97, 55, 216, 95, 199, 234, 182, 192, 45, 24, 166, 45, 157, 177, 21, 213, 109, 64, 53, 112, 211, 32, 108, 236, 110, 3, 0, 54, 76, 48, 33, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_COMPRESSED_UPDATE_OBJECT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 4)
        r.write_encrypted_server(written, NullHeaderCrypto())


class SMSG_ACCOUNT_DATA_TIMES_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 130, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_ACCOUNT_DATA_TIMES)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_REQUEST_ACCOUNT_DATA_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 10, 2, 0, 0, 6, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_REQUEST_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_UPDATE_ACCOUNT_DATA_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 11, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_UPDATE_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_encrypted_client(written, NullHeaderCrypto())

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([4, 160, 11, 2, 0, 0, 7, 0, 0, 0, 24, 20, 0, 0, 120, 1, 189, 87, 219, 150, 171, 40, 16, 125, 231, 43, 252, 4, 181, 147, 182, 243, 72, 20, 35, 211, 68, 178, 4, 59, 39, 231, 133, 255, 255, 139, 41, 174, 130, 74, 39, 15, 51, 89, 221, 174, 104, 93, 54, 80, 84, 21, 155, 31, 50, 9, 202, 199, 162, 70, 8, 119, 29, 233, 126, 150, 111, 126, 147, 160, 81, 151, 153, 178, 78, 77, 164, 157, 102, 42, 175, 100, 148, 170, 29, 240, 56, 18, 86, 224, 89, 114, 132, 220, 151, 64, 100, 236, 16, 250, 203, 71, 226, 37, 69, 93, 158, 154, 234, 120, 4, 27, 206, 248, 36, 144, 192, 143, 162, 62, 30, 253, 131, 110, 120, 146, 143, 162, 106, 74, 243, 128, 6, 77, 152, 118, 70, 93, 213, 77, 81, 34, 51, 118, 241, 121, 48, 162, 207, 3, 226, 125, 79, 91, 50, 105, 73, 117, 170, 225, 7, 61, 8, 99, 78, 171, 63, 239, 3, 21, 55, 48, 208, 163, 84, 245, 151, 254, 245, 50, 69, 199, 158, 79, 215, 68, 69, 174, 92, 146, 32, 1, 127, 73, 254, 72, 181, 145, 138, 135, 144, 196, 122, 106, 224, 18, 93, 249, 8, 146, 73, 197, 11, 170, 142, 167, 32, 95, 205, 202, 155, 111, 128, 125, 36, 205, 116, 97, 65, 176, 40, 31, 79, 245, 15, 167, 163, 89, 165, 94, 7, 60, 65, 193, 8, 254, 33, 251, 26, 42, 228, 174, 98, 228, 18, 226, 102, 85, 171, 97, 172, 74, 205, 2, 162, 166, 99, 234, 30, 132, 251, 239, 16, 24, 29, 197, 110, 244, 27, 99, 163, 74, 47, 35, 159, 136, 149, 149, 16, 18, 241, 77, 97, 39, 190, 142, 250, 95, 219, 51, 206, 101, 97, 55, 182, 132, 253, 191, 158, 177, 84, 87, 42, 90, 179, 13, 102, 111, 252, 254, 248, 232, 248, 189, 171, 154, 19, 228, 131, 121, 188, 163, 32, 172, 87, 3, 149, 194, 76, 73, 71, 75, 15, 225, 80, 141, 18, 160, 5, 217, 85, 223, 136, 204, 186, 106, 221, 47, 158, 58, 61, 243, 190, 70, 155, 247, 238, 39, 10, 21, 193, 30, 55, 134, 31, 144, 42, 185, 217, 175, 204, 242, 120, 3, 23, 146, 50, 242, 4, 46, 181, 202, 163, 181, 19, 193, 114, 158, 136, 250, 17, 42, 141, 238, 161, 41, 14, 141, 143, 237, 198, 44, 66, 204, 26, 154, 178, 206, 46, 56, 134, 180, 150, 17, 230, 106, 107, 99, 219, 240, 158, 139, 100, 48, 128, 37, 133, 247, 60, 182, 15, 188, 234, 32, 18, 195, 94, 98, 185, 88, 230, 13, 254, 220, 212, 5, 235, 42, 173, 42, 243, 232, 164, 132, 246, 195, 152, 13, 105, 135, 175, 248, 98, 219, 139, 94, 23, 212, 200, 162, 59, 207, 125, 31, 198, 244, 26, 157, 142, 43, 167, 5, 82, 43, 19, 175, 72, 101, 82, 49, 239, 105, 212, 25, 95, 31, 6, 151, 87, 89, 144, 149, 93, 6, 45, 77, 191, 44, 88, 106, 150, 193, 10, 123, 232, 83, 212, 195, 149, 117, 209, 124, 22, 117, 213, 184, 128, 110, 12, 95, 0, 180, 153, 231, 17, 109, 67, 49, 77, 197, 238, 81, 12, 105, 77, 95, 192, 12, 78, 47, 193, 6, 235, 12, 178, 156, 112, 71, 76, 87, 77, 219, 154, 157, 160, 29, 66, 12, 148, 176, 78, 40, 56, 166, 117, 17, 135, 132, 90, 82, 99, 99, 199, 229, 0, 71, 252, 142, 37, 158, 39, 172, 46, 112, 124, 231, 160, 22, 3, 19, 145, 95, 33, 204, 40, 59, 22, 20, 206, 81, 69, 70, 125, 238, 25, 46, 177, 55, 145, 51, 180, 166, 111, 165, 71, 219, 1, 128, 195, 157, 242, 142, 182, 187, 21, 182, 44, 59, 53, 211, 17, 222, 27, 41, 88, 61, 201, 134, 149, 221, 83, 184, 85, 173, 100, 211, 33, 224, 174, 28, 158, 14, 144, 214, 207, 115, 252, 212, 254, 41, 124, 72, 205, 231, 200, 193, 52, 7, 218, 99, 56, 180, 58, 197, 120, 139, 153, 237, 49, 201, 174, 186, 51, 124, 224, 192, 38, 108, 51, 173, 107, 160, 123, 80, 226, 85, 137, 206, 23, 101, 169, 151, 26, 201, 12, 245, 96, 153, 94, 85, 3, 173, 136, 149, 152, 49, 138, 71, 224, 55, 154, 110, 128, 243, 199, 41, 242, 28, 248, 212, 217, 30, 172, 89, 138, 27, 174, 199, 173, 225, 182, 58, 15, 161, 67, 59, 134, 165, 39, 166, 41, 28, 89, 88, 106, 105, 24, 169, 2, 202, 213, 57, 86, 89, 87, 192, 76, 190, 62, 172, 252, 142, 167, 145, 142, 23, 187, 34, 167, 0, 146, 73, 128, 28, 41, 233, 153, 169, 231, 57, 154, 219, 170, 51, 23, 34, 34, 152, 30, 173, 167, 12, 248, 100, 68, 167, 128, 46, 73, 70, 46, 19, 159, 3, 239, 210, 132, 56, 22, 239, 205, 202, 17, 202, 202, 204, 200, 83, 57, 39, 172, 247, 132, 31, 123, 66, 203, 183, 87, 238, 150, 182, 175, 132, 208, 134, 161, 119, 174, 132, 205, 158, 208, 176, 198, 181, 229, 105, 207, 178, 42, 19, 169, 185, 86, 220, 233, 216, 241, 123, 81, 33, 65, 255, 194, 62, 195, 62, 194, 133, 2, 246, 219, 252, 1, 215, 108, 191, 33, 118, 21, 234, 252, 139, 24, 248, 29, 206, 101, 132, 174, 68, 8, 56, 132, 225, 238, 97, 56, 188, 190, 130, 152, 59, 131, 191, 21, 216, 59, 136, 189, 104, 32, 159, 204, 158, 106, 91, 82, 107, 168, 172, 189, 221, 184, 72, 254, 122, 215, 137, 231, 91, 191, 54, 95, 48, 51, 243, 45, 163, 249, 174, 41, 179, 79, 221, 64, 214, 18, 129, 165, 57, 94, 228, 41, 111, 252, 157, 90, 164, 13, 65, 51, 42, 111, 155, 106, 82, 47, 31, 159, 132, 52, 122, 199, 141, 50, 245, 245, 45, 206, 178, 41, 239, 228, 70, 75, 133, 142, 86, 197, 116, 201, 54, 162, 88, 162, 251, 141, 251, 94, 104, 83, 36, 136, 244, 233, 146, 18, 168, 84, 21, 249, 108, 86, 147, 184, 109, 180, 145, 103, 116, 110, 187, 233, 88, 215, 213, 89, 237, 116, 203, 161, 170, 55, 214, 9, 55, 167, 164, 147, 47, 39, 163, 19, 132, 3, 196, 100, 69, 50, 197, 84, 165, 231, 7, 53, 96, 248, 103, 208, 164, 139, 223, 247, 78, 109, 118, 97, 66, 48, 246, 17, 130, 218, 58, 111, 26, 190, 79, 133, 180, 39, 219, 62, 252, 180, 234, 160, 98, 226, 122, 251, 120, 173, 222, 128, 111, 111, 234, 205, 192, 252, 82, 223, 171, 145, 14, 111, 27, 9, 174, 20, 175, 244, 188, 255, 96, 77, 159, 111, 27, 9, 152, 251, 155, 214, 244, 245, 182, 145, 78, 111, 27, 9, 200, 207, 255, 30, 190, 127, 1, 52, 153, 2, 36, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_UPDATE_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_encrypted_client(written, NullHeaderCrypto())


class CMSG_GMTICKET_GETTICKET_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 17, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_GMTICKET_GETTICKET)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGIN_VERIFY_WORLD_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 22, 54, 2, 0, 0, 0, 0, 205, 215, 11, 198, 53, 126, 4, 195, 249, 15, 167, 66, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_LOGIN_VERIFY_WORLD)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_LEARN_TALENT_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 81, 2, 0, 0, 158, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_LEARN_TALENT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_AUCTION_HELLO_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 85, 2, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_AUCTION_HELLO_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SET_ACTIVE_MOVER_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 106, 2, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_SET_ACTIVE_MOVER)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_QUERY_NEXT_MAIL_TIME_Client_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 132, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.MSG_QUERY_NEXT_MAIL_TIME_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_MEETINGSTONE_INFO_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 150, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_MEETINGSTONE_INFO)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_RENAME_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 21, 199, 2, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, 68, 101, 97, 100, 98, 101, 101, 102, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_CHAR_RENAME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_CHAR_RENAME_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 200, 2, 71, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHAR_RENAME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 20, 200, 2, 0, 239, 190, 173, 222, 0, 0, 0, 0, 68, 101, 97, 100, 98, 101, 101, 102, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_CHAR_RENAME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_REQUEST_RAID_INFO_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 205, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_REQUEST_RAID_INFO)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_MOVE_TIME_SKIPPED_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 16, 206, 2, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_MOVE_TIME_SKIPPED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_BATTLEFIELD_STATUS_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 211, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_client_opcode_unencrypted(reader, vanilla.CMSG_BATTLEFIELD_STATUS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_COMPRESSED_MOVES_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 50, 251, 2, 46, 0, 0, 0, 120, 1, 211, 189, 203, 192, 40, 145, 183, 154, 251, 216, 186, 88, 230, 195, 43, 212, 151, 59, 49, 32, 3, 70, 32, 167, 100, 57, 247, 177, 245, 239, 95, 29, 58, 121, 102, 137, 19, 0, 38, 30, 14, 73, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_COMPRESSED_MOVES)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 4)
        r.write_encrypted_server(written, NullHeaderCrypto())

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 70, 251, 2, 59, 0, 0, 0, 120, 1, 179, 186, 203, 112, 59, 95, 198, 65, 220, 224, 99, 245, 27, 177, 35, 215, 23, 55, 31, 109, 80, 148, 113, 210, 87, 100, 0, 2, 70, 6, 134, 99, 28, 12, 12, 204, 64, 102, 235, 107, 177, 35, 92, 229, 205, 71, 21, 183, 203, 58, 49, 20, 0, 5, 12, 24, 24, 0, 88, 227, 17, 4, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_COMPRESSED_MOVES)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 4)
        r.write_encrypted_server(written, NullHeaderCrypto())


class SMSG_SPLINE_SET_RUN_SPEED_vanilla(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 254, 2, 1, 6, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await vanilla.expect_server_opcode_unencrypted(reader, vanilla.SMSG_SPLINE_SET_RUN_SPEED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_TELEPORT_TO_UNIT_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 11, 9, 0, 0, 0, 86, 117, 114, 116, 110, 101, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_TELEPORT_TO_UNIT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_ENUM_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 55, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CHAR_ENUM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_DELETE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 56, 0, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CHAR_DELETE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PLAYER_LOGIN_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 61, 0, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_PLAYER_LOGIN)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGIN_SETTIMESPEED_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 66, 0, 10, 50, 115, 22, 137, 136, 136, 60, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_LOGIN_SETTIMESPEED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PLAYER_LOGOUT_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 74, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_PLAYER_LOGOUT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_LOGOUT_REQUEST_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 75, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_LOGOUT_REQUEST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGOUT_RESPONSE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 7, 76, 0, 0, 0, 0, 0, 1, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_LOGOUT_RESPONSE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_LOGOUT_COMPLETE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 2, 77, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_LOGOUT_COMPLETE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PET_NAME_QUERY_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 16, 82, 0, 0, 0, 239, 190, 173, 222, 239, 190, 173, 222, 222, 202, 250, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_PET_NAME_QUERY)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_DESTROY_OBJECT_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 170, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_DESTROY_OBJECT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_MOVE_TELEPORT_ACK_Client_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 13, 199, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.MSG_MOVE_TELEPORT_ACK_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_TUTORIAL_FLAGS_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 34, 253, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_TUTORIAL_FLAGS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_STANDSTATECHANGE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 1, 1, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_STANDSTATECHANGE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_AUTOEQUIP_ITEM_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 10, 1, 0, 0, 255, 24, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_AUTOEQUIP_ITEM)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_INITIATE_TRADE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 22, 1, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_INITIATE_TRADE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CANCEL_TRADE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 28, 1, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CANCEL_TRADE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_INITIAL_SPELLS_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 167, 42, 1, 0, 40, 0, 78, 0, 0, 0, 81, 0, 0, 0, 107, 0, 0, 0, 196, 0, 0, 0, 198, 0, 0, 0, 201, 0, 0, 0, 203, 0, 0, 0, 204, 0, 0, 0, 10, 2, 0, 0, 156, 2, 0, 0, 78, 9, 0, 0, 153, 9, 0, 0, 175, 9, 0, 0, 234, 11, 0, 0, 37, 13, 0, 0, 181, 20, 0, 0, 89, 24, 0, 0, 102, 24, 0, 0, 103, 24, 0, 0, 77, 25, 0, 0, 78, 25, 0, 0, 203, 25, 0, 0, 98, 28, 0, 0, 99, 28, 0, 0, 187, 28, 0, 0, 194, 32, 0, 0, 33, 34, 0, 0, 117, 35, 0, 0, 118, 35, 0, 0, 156, 35, 0, 0, 165, 35, 0, 0, 117, 80, 0, 0, 118, 80, 0, 0, 119, 80, 0, 0, 120, 80, 0, 0, 128, 81, 0, 0, 147, 84, 0, 0, 148, 84, 0, 0, 11, 86, 0, 0, 26, 89, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_INITIAL_SPELLS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CANCEL_CAST_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 47, 1, 0, 0, 120, 80, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CANCEL_CAST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 47, 1, 0, 0, 242, 33, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CANCEL_CAST)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SET_SELECTION_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 61, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_SET_SELECTION)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_ATTACKSWING_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 65, 1, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_ATTACKSWING)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ATTACKSTART_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 18, 67, 1, 23, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_ATTACKSTART)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_ATTACKSTOP_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 10, 68, 1, 1, 23, 1, 100, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_ATTACKSTOP)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_QUERY_TIME_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 206, 1, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_QUERY_TIME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_PING_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 220, 1, 0, 0, 239, 190, 173, 222, 222, 202, 250, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_PING)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_PONG_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 221, 1, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_PONG)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SETSHEATHED_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 224, 1, 0, 0, 1, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_SETSHEATHED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_AUTH_CHALLENGE_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 6, 236, 1, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_AUTH_CHALLENGE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_unencrypted(written)
        self.assertEqual(data, written)


class CMSG_AUTH_SESSION_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 172, 237, 1, 0, 0, 243, 22, 0, 0, 0, 0, 0, 0, 65, 0, 136, 2, 216, 73, 136, 157, 239, 5, 37, 187, 193, 171, 167, 138, 219, 164, 251, 163, 231, 126, 103, 172, 234, 198, 86, 1, 0, 0, 120, 156, 117, 204, 189, 14, 194, 48, 12, 4, 224, 242, 30, 188, 12, 97, 64, 149, 200, 66, 195, 140, 76, 226, 34, 11, 199, 169, 140, 203, 79, 159, 30, 22, 36, 6, 115, 235, 119, 119, 129, 105, 89, 64, 203, 105, 51, 103, 163, 38, 199, 190, 91, 213, 199, 122, 223, 125, 18, 190, 22, 192, 140, 113, 36, 228, 18, 73, 168, 194, 228, 149, 72, 10, 201, 197, 61, 216, 182, 122, 6, 75, 248, 52, 15, 21, 70, 115, 103, 187, 56, 204, 122, 199, 151, 139, 189, 220, 38, 204, 254, 48, 66, 214, 230, 202, 1, 168, 184, 144, 128, 81, 252, 183, 164, 80, 112, 184, 18, 243, 63, 38, 65, 253, 181, 55, 144, 25, 102, 143, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_AUTH_SESSION)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_unencrypted(written)


class SMSG_ACCOUNT_DATA_TIMES_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 130, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_ACCOUNT_DATA_TIMES)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_REQUEST_ACCOUNT_DATA_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 10, 2, 0, 0, 6, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_REQUEST_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_UPDATE_ACCOUNT_DATA_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 11, 2, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_UPDATE_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_encrypted_client(written, NullHeaderCrypto())

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([4, 160, 11, 2, 0, 0, 7, 0, 0, 0, 24, 20, 0, 0, 120, 1, 189, 87, 219, 150, 171, 40, 16, 125, 231, 43, 252, 4, 181, 147, 182, 243, 72, 20, 35, 211, 68, 178, 4, 59, 39, 231, 133, 255, 255, 139, 41, 174, 130, 74, 39, 15, 51, 89, 221, 174, 104, 93, 54, 80, 84, 21, 155, 31, 50, 9, 202, 199, 162, 70, 8, 119, 29, 233, 126, 150, 111, 126, 147, 160, 81, 151, 153, 178, 78, 77, 164, 157, 102, 42, 175, 100, 148, 170, 29, 240, 56, 18, 86, 224, 89, 114, 132, 220, 151, 64, 100, 236, 16, 250, 203, 71, 226, 37, 69, 93, 158, 154, 234, 120, 4, 27, 206, 248, 36, 144, 192, 143, 162, 62, 30, 253, 131, 110, 120, 146, 143, 162, 106, 74, 243, 128, 6, 77, 152, 118, 70, 93, 213, 77, 81, 34, 51, 118, 241, 121, 48, 162, 207, 3, 226, 125, 79, 91, 50, 105, 73, 117, 170, 225, 7, 61, 8, 99, 78, 171, 63, 239, 3, 21, 55, 48, 208, 163, 84, 245, 151, 254, 245, 50, 69, 199, 158, 79, 215, 68, 69, 174, 92, 146, 32, 1, 127, 73, 254, 72, 181, 145, 138, 135, 144, 196, 122, 106, 224, 18, 93, 249, 8, 146, 73, 197, 11, 170, 142, 167, 32, 95, 205, 202, 155, 111, 128, 125, 36, 205, 116, 97, 65, 176, 40, 31, 79, 245, 15, 167, 163, 89, 165, 94, 7, 60, 65, 193, 8, 254, 33, 251, 26, 42, 228, 174, 98, 228, 18, 226, 102, 85, 171, 97, 172, 74, 205, 2, 162, 166, 99, 234, 30, 132, 251, 239, 16, 24, 29, 197, 110, 244, 27, 99, 163, 74, 47, 35, 159, 136, 149, 149, 16, 18, 241, 77, 97, 39, 190, 142, 250, 95, 219, 51, 206, 101, 97, 55, 182, 132, 253, 191, 158, 177, 84, 87, 42, 90, 179, 13, 102, 111, 252, 254, 248, 232, 248, 189, 171, 154, 19, 228, 131, 121, 188, 163, 32, 172, 87, 3, 149, 194, 76, 73, 71, 75, 15, 225, 80, 141, 18, 160, 5, 217, 85, 223, 136, 204, 186, 106, 221, 47, 158, 58, 61, 243, 190, 70, 155, 247, 238, 39, 10, 21, 193, 30, 55, 134, 31, 144, 42, 185, 217, 175, 204, 242, 120, 3, 23, 146, 50, 242, 4, 46, 181, 202, 163, 181, 19, 193, 114, 158, 136, 250, 17, 42, 141, 238, 161, 41, 14, 141, 143, 237, 198, 44, 66, 204, 26, 154, 178, 206, 46, 56, 134, 180, 150, 17, 230, 106, 107, 99, 219, 240, 158, 139, 100, 48, 128, 37, 133, 247, 60, 182, 15, 188, 234, 32, 18, 195, 94, 98, 185, 88, 230, 13, 254, 220, 212, 5, 235, 42, 173, 42, 243, 232, 164, 132, 246, 195, 152, 13, 105, 135, 175, 248, 98, 219, 139, 94, 23, 212, 200, 162, 59, 207, 125, 31, 198, 244, 26, 157, 142, 43, 167, 5, 82, 43, 19, 175, 72, 101, 82, 49, 239, 105, 212, 25, 95, 31, 6, 151, 87, 89, 144, 149, 93, 6, 45, 77, 191, 44, 88, 106, 150, 193, 10, 123, 232, 83, 212, 195, 149, 117, 209, 124, 22, 117, 213, 184, 128, 110, 12, 95, 0, 180, 153, 231, 17, 109, 67, 49, 77, 197, 238, 81, 12, 105, 77, 95, 192, 12, 78, 47, 193, 6, 235, 12, 178, 156, 112, 71, 76, 87, 77, 219, 154, 157, 160, 29, 66, 12, 148, 176, 78, 40, 56, 166, 117, 17, 135, 132, 90, 82, 99, 99, 199, 229, 0, 71, 252, 142, 37, 158, 39, 172, 46, 112, 124, 231, 160, 22, 3, 19, 145, 95, 33, 204, 40, 59, 22, 20, 206, 81, 69, 70, 125, 238, 25, 46, 177, 55, 145, 51, 180, 166, 111, 165, 71, 219, 1, 128, 195, 157, 242, 142, 182, 187, 21, 182, 44, 59, 53, 211, 17, 222, 27, 41, 88, 61, 201, 134, 149, 221, 83, 184, 85, 173, 100, 211, 33, 224, 174, 28, 158, 14, 144, 214, 207, 115, 252, 212, 254, 41, 124, 72, 205, 231, 200, 193, 52, 7, 218, 99, 56, 180, 58, 197, 120, 139, 153, 237, 49, 201, 174, 186, 51, 124, 224, 192, 38, 108, 51, 173, 107, 160, 123, 80, 226, 85, 137, 206, 23, 101, 169, 151, 26, 201, 12, 245, 96, 153, 94, 85, 3, 173, 136, 149, 152, 49, 138, 71, 224, 55, 154, 110, 128, 243, 199, 41, 242, 28, 248, 212, 217, 30, 172, 89, 138, 27, 174, 199, 173, 225, 182, 58, 15, 161, 67, 59, 134, 165, 39, 166, 41, 28, 89, 88, 106, 105, 24, 169, 2, 202, 213, 57, 86, 89, 87, 192, 76, 190, 62, 172, 252, 142, 167, 145, 142, 23, 187, 34, 167, 0, 146, 73, 128, 28, 41, 233, 153, 169, 231, 57, 154, 219, 170, 51, 23, 34, 34, 152, 30, 173, 167, 12, 248, 100, 68, 167, 128, 46, 73, 70, 46, 19, 159, 3, 239, 210, 132, 56, 22, 239, 205, 202, 17, 202, 202, 204, 200, 83, 57, 39, 172, 247, 132, 31, 123, 66, 203, 183, 87, 238, 150, 182, 175, 132, 208, 134, 161, 119, 174, 132, 205, 158, 208, 176, 198, 181, 229, 105, 207, 178, 42, 19, 169, 185, 86, 220, 233, 216, 241, 123, 81, 33, 65, 255, 194, 62, 195, 62, 194, 133, 2, 246, 219, 252, 1, 215, 108, 191, 33, 118, 21, 234, 252, 139, 24, 248, 29, 206, 101, 132, 174, 68, 8, 56, 132, 225, 238, 97, 56, 188, 190, 130, 152, 59, 131, 191, 21, 216, 59, 136, 189, 104, 32, 159, 204, 158, 106, 91, 82, 107, 168, 172, 189, 221, 184, 72, 254, 122, 215, 137, 231, 91, 191, 54, 95, 48, 51, 243, 45, 163, 249, 174, 41, 179, 79, 221, 64, 214, 18, 129, 165, 57, 94, 228, 41, 111, 252, 157, 90, 164, 13, 65, 51, 42, 111, 155, 106, 82, 47, 31, 159, 132, 52, 122, 199, 141, 50, 245, 245, 45, 206, 178, 41, 239, 228, 70, 75, 133, 142, 86, 197, 116, 201, 54, 162, 88, 162, 251, 141, 251, 94, 104, 83, 36, 136, 244, 233, 146, 18, 168, 84, 21, 249, 108, 86, 147, 184, 109, 180, 145, 103, 116, 110, 187, 233, 88, 215, 213, 89, 237, 116, 203, 161, 170, 55, 214, 9, 55, 167, 164, 147, 47, 39, 163, 19, 132, 3, 196, 100, 69, 50, 197, 84, 165, 231, 7, 53, 96, 248, 103, 208, 164, 139, 223, 247, 78, 109, 118, 97, 66, 48, 246, 17, 130, 218, 58, 111, 26, 190, 79, 133, 180, 39, 219, 62, 252, 180, 234, 160, 98, 226, 122, 251, 120, 173, 222, 128, 111, 111, 234, 205, 192, 252, 82, 223, 171, 145, 14, 111, 27, 9, 174, 20, 175, 244, 188, 255, 96, 77, 159, 111, 27, 9, 152, 251, 155, 214, 244, 245, 182, 145, 78, 111, 27, 9, 200, 207, 255, 30, 190, 127, 1, 52, 153, 2, 36, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_UPDATE_ACCOUNT_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(r.size() + 6)
        r.write_encrypted_client(written, NullHeaderCrypto())


class CMSG_GMTICKET_GETTICKET_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 17, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_GMTICKET_GETTICKET)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_AUCTION_HELLO_Client_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 85, 2, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.MSG_AUCTION_HELLO_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_SET_ACTIVE_MOVER_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 12, 106, 2, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_SET_ACTIVE_MOVER)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class MSG_QUERY_NEXT_MAIL_TIME_Client_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 132, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.MSG_QUERY_NEXT_MAIL_TIME_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_MEETINGSTONE_INFO_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 150, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_MEETINGSTONE_INFO)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_CHAR_RENAME_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 21, 199, 2, 0, 0, 239, 190, 173, 222, 0, 0, 0, 0, 68, 101, 97, 100, 98, 101, 101, 102, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_CHAR_RENAME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 6, r.size())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_REQUEST_RAID_INFO_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 205, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_REQUEST_RAID_INFO)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_MOVE_TIME_SKIPPED_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 16, 206, 2, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_MOVE_TIME_SKIPPED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class CMSG_BATTLEFIELD_STATUS_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 4, 211, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_client_opcode_unencrypted(reader, tbc.CMSG_BATTLEFIELD_STATUS)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write_encrypted_client(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_SPLINE_SET_RUN_SPEED_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 8, 254, 2, 1, 6, 0, 0, 224, 64, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_SPLINE_SET_RUN_SPEED)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


class SMSG_MOTD_tbc(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 116, 61, 3, 2, 0, 0, 0, 87, 101, 108, 99, 111, 109, 101, 32, 116, 111, 32, 97, 110, 32, 65, 122, 101, 114, 111, 116, 104, 67, 111, 114, 101, 32, 115, 101, 114, 118, 101, 114, 46, 0, 124, 99, 102, 102, 70, 70, 52, 65, 50, 68, 84, 104, 105, 115, 32, 115, 101, 114, 118, 101, 114, 32, 114, 117, 110, 115, 32, 111, 110, 32, 65, 122, 101, 114, 111, 116, 104, 67, 111, 114, 101, 124, 114, 32, 124, 99, 102, 102, 51, 67, 69, 55, 70, 70, 119, 119, 119, 46, 97, 122, 101, 114, 111, 116, 104, 99, 111, 114, 101, 46, 111, 114, 103, 124, 114, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await tbc.expect_server_opcode_unencrypted(reader, tbc.SMSG_MOTD)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write_encrypted_server(written, NullHeaderCrypto())
        self.assertEqual(data, written)


