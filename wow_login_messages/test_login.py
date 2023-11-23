import asyncio
import unittest

import wow_login_messages.version2
import wow_login_messages.version3
import wow_login_messages.version5
import wow_login_messages.version8
import wow_login_messages.all


class CMD_AUTH_LOGON_CHALLENGE_Server0(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_CHALLENGE_Server1(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 1, 239, 190, 173, 222, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_server_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_server_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_CHALLENGE_Server3(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 1, 239, 190, 173, 222, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 4, 1, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test3(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 2, 255, 238, 221, 204, 222, 202, 250, 239, 190, 173, 222, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test4(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 5, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test5(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 73, 216, 194, 188, 104, 92, 43, 206, 74, 244, 250, 7, 10, 71, 147, 120, 88, 120, 70, 181, 131, 212, 65, 130, 158, 36, 216, 135, 206, 218, 52, 70, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 199, 9, 135, 125, 140, 101, 82, 102, 165, 125, 184, 101, 61, 110, 166, 43, 181, 84, 242, 11, 207, 116, 214, 74, 119, 167, 211, 61, 243, 48, 144, 135, 186, 163, 30, 153, 160, 11, 33, 87, 252, 55, 63, 179, 105, 205, 210, 241, 6, 255, 238, 221, 204, 222, 202, 250, 239, 190, 173, 222, 0, 1, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test6(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 5, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_CHALLENGE_Client4(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 3, 31, 0, 87, 111, 87, 0, 1, 12, 1, 243, 22, 54, 56, 120, 0, 110, 105, 87, 0, 66, 71, 110, 101, 60, 0, 0, 0, 127, 0, 0, 1, 1, 65, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.all.expect_client_opcode(reader, wow_login_messages.all.CMD_AUTH_LOGON_CHALLENGE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Client5(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 2, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 254, 0, 238, 190, 173, 222, 0, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 1, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Server6(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 239, 190, 173, 222, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_LOGON_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Client7(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 2, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 254, 0, 238, 190, 173, 222, 0, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_client_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 1, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_client_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_client_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test3(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_client_opcode(reader, wow_login_messages.version3.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Client10(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 2, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 254, 0, 238, 190, 173, 222, 0, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_client_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 1, 255, 0, 239, 190, 173, 222, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_client_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_client_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test3(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 241, 62, 229, 209, 131, 196, 200, 169, 80, 14, 63, 90, 93, 138, 238, 78, 46, 69, 225, 247, 204, 143, 28, 245, 238, 142, 17, 206, 211, 29, 215, 8, 107, 30, 72, 27, 77, 4, 161, 24, 216, 242, 222, 92, 89, 213, 92, 129, 46, 101, 236, 62, 78, 245, 45, 225, 128, 94, 26, 103, 21, 236, 200, 65, 238, 184, 144, 138, 88, 187, 0, 208, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_client_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Server11(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 7, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 8, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_LOGON_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_CHALLENGE_Server12(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 3, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_CHALLENGE_Server13(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_RECONNECT_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 3, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_RECONNECT_CHALLENGE_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_CHALLENGE_Client14(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 2, 31, 0, 87, 111, 87, 0, 1, 12, 1, 243, 22, 54, 56, 120, 0, 110, 105, 87, 0, 66, 71, 110, 101, 60, 0, 0, 0, 127, 0, 0, 1, 1, 65, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.all.expect_client_opcode(reader, wow_login_messages.all.CMD_AUTH_RECONNECT_CHALLENGE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([2, 2, 46, 0, 87, 111, 87, 0, 1, 12, 1, 243, 22, 54, 56, 120, 0, 110, 105, 87, 0, 66, 71, 110, 101, 60, 0, 0, 0, 127, 0, 0, 1, 16, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.all.expect_client_opcode(reader, wow_login_messages.all.CMD_AUTH_RECONNECT_CHALLENGE_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 4, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_PROOF_Server15(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 14, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test2(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 14, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_PROOF_Client16(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 234, 250, 185, 198, 24, 21, 11, 242, 249, 50, 206, 39, 98, 121, 150, 153, 107, 109, 26, 13, 243, 165, 158, 106, 56, 2, 231, 11, 225, 47, 5, 113, 186, 71, 140, 163, 40, 167, 158, 154, 36, 40, 230, 130, 237, 236, 199, 201, 232, 110, 241, 59, 123, 225, 224, 245, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_AUTH_RECONNECT_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_RECONNECT_PROOF_Server18(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_RECONNECT_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 16, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_AUTH_RECONNECT_PROOF_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_SURVEY_RESULT19(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([4, 222, 250, 0, 0, 0, 1, 0, 255, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version3.expect_client_opcode(reader, wow_login_messages.version3.CMD_SURVEY_RESULT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_REALM_LIST_Server20(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 23, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 65, 0, 65, 0, 0, 0, 200, 67, 1, 0, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 23, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 65, 0, 65, 0, 0, 0, 200, 67, 1, 0, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_REALM_LIST_Client21(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_REALM_LIST_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_REALM_LIST_Server23(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 22, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 65, 0, 65, 0, 0, 0, 200, 67, 1, 0, 2, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)

    async def test1(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 27, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 65, 0, 65, 0, 0, 0, 200, 67, 1, 0, 2, 1, 12, 1, 243, 22, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version8.expect_server_opcode(reader, wow_login_messages.version8.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


