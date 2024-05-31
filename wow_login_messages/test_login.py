import asyncio
import unittest

import wow_login_messages.version2
import wow_login_messages.version3
import wow_login_messages.version5
import wow_login_messages.version8
import wow_login_messages.all
import wow_login_messages.version6


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


class CMD_AUTH_LOGON_CHALLENGE_Server2(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([0, 0, 0, 58, 43, 237, 162, 169, 101, 37, 78, 69, 4, 195, 168, 246, 106, 134, 201, 81, 114, 215, 99, 107, 54, 137, 237, 192, 63, 252, 193, 66, 165, 121, 50, 1, 7, 32, 183, 155, 62, 42, 135, 130, 60, 171, 143, 94, 191, 191, 142, 177, 1, 8, 83, 80, 6, 41, 139, 91, 173, 189, 91, 83, 225, 137, 94, 100, 75, 137, 174, 120, 124, 96, 218, 20, 21, 219, 130, 36, 67, 72, 71, 108, 63, 211, 188, 22, 60, 89, 21, 128, 86, 5, 146, 59, 82, 46, 114, 18, 41, 82, 70, 15, 184, 237, 114, 71, 169, 255, 31, 242, 228, 96, 253, 255, 127, 249, 3, 0, 0, 0, 0, 89, 29, 166, 11, 52, 253, 100, 94, 56, 108, 84, 192, 24, 182, 167, 47, 8, 8, 2, 1, 194, 216, 23, 56, 5, 251, 84, 143, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version5.expect_server_opcode(reader, wow_login_messages.version5.CMD_AUTH_LOGON_CHALLENGE_Server)
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


class CMD_AUTH_LOGON_PROOF_Client8(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 4, 73, 87, 221, 32, 81, 98, 245, 250, 254, 179, 103, 7, 114, 9, 81, 86, 32, 8, 8, 32, 193, 38, 202, 200, 247, 59, 70, 251, 136, 50, 6, 130, 201, 151, 96, 66, 228, 117, 249, 124, 96, 98, 228, 84, 102, 166, 254, 220, 233, 170, 124, 254, 116, 218, 112, 136, 204, 118, 36, 196, 40, 136, 181, 239, 196, 29, 180, 107, 197, 44, 251, 0, 3, 221, 105, 240, 247, 88, 76, 88, 240, 134, 54, 58, 26, 190, 110, 30, 77, 90, 78, 192, 86, 88, 136, 230, 41, 1, 108, 191, 61, 247, 142, 130, 147, 111, 29, 190, 229, 105, 52, 205, 8, 130, 148, 239, 93, 15, 150, 159, 252, 23, 11, 228, 66, 8, 46, 209, 16, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version5.expect_client_opcode(reader, wow_login_messages.version5.CMD_AUTH_LOGON_PROOF_Client)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_AUTH_LOGON_PROOF_Server9(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([1, 0, 25, 255, 233, 250, 100, 169, 155, 175, 246, 179, 141, 156, 17, 171, 220, 174, 128, 196, 210, 231, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version5.expect_server_opcode(reader, wow_login_messages.version5.CMD_AUTH_LOGON_PROOF_Server)
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


class CMD_AUTH_RECONNECT_PROOF_Server17(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([3, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version5.expect_server_opcode(reader, wow_login_messages.version5.CMD_AUTH_RECONNECT_PROOF_Server)
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


class CMD_REALM_LIST_Server22(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 80, 0, 0, 0, 0, 0, 2, 0, 0, 0, 84, 101, 115, 116, 32, 82, 101, 97, 108, 109, 50, 0, 108, 111, 99, 97, 108, 104, 111, 115, 116, 58, 56, 48, 56, 53, 0, 0, 0, 72, 67, 3, 1, 1, 0, 0, 0, 84, 101, 115, 116, 32, 82, 101, 97, 108, 109, 0, 108, 111, 99, 97, 108, 104, 111, 115, 116, 58, 56, 48, 56, 53, 0, 0, 0, 72, 67, 3, 2, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version5.expect_server_opcode(reader, wow_login_messages.version5.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_REALM_LIST_Server23(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([16, 81, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 84, 101, 115, 116, 32, 82, 101, 97, 108, 109, 50, 0, 108, 111, 99, 97, 108, 104, 111, 115, 116, 58, 56, 48, 56, 53, 0, 0, 0, 72, 67, 3, 1, 1, 0, 0, 0, 84, 101, 115, 116, 32, 82, 101, 97, 108, 109, 0, 108, 111, 99, 97, 108, 104, 111, 115, 116, 58, 56, 48, 56, 53, 0, 0, 0, 72, 67, 3, 2, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version6.expect_server_opcode(reader, wow_login_messages.version6.CMD_REALM_LIST_Server)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        self.assertEqual(len(data) - 3, r.size())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_REALM_LIST_Server24(unittest.IsolatedAsyncioTestCase):
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


class CMD_XFER_INITIATE25(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([48, 5, 80, 97, 116, 99, 104, 188, 9, 0, 0, 0, 0, 0, 0, 17, 91, 85, 89, 127, 183, 223, 14, 134, 217, 179, 174, 90, 235, 203, 98, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_XFER_INITIATE)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_XFER_DATA26(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([49, 64, 0, 77, 80, 81, 26, 44, 0, 0, 0, 60, 224, 38, 0, 1, 0, 3, 0, 252, 217, 38, 0, 252, 221, 38, 0, 64, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 120, 218, 236, 125, 123, 124, 84, 197, 245, 248, 110, 246, 134, 92, 116, 37, 11, 174, 184, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_server_opcode(reader, wow_login_messages.version2.CMD_XFER_DATA)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_XFER_ACCEPT27(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([50, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_XFER_ACCEPT)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_XFER_RESUME28(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([51, 64, 0, 0, 0, 0, 0, 0, 0, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_XFER_RESUME)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


class CMD_XFER_CANCEL29(unittest.IsolatedAsyncioTestCase):
    async def test0(self):
        reader = asyncio.StreamReader()

        data = bytes([52, ])

        reader.feed_data(data)
        reader.feed_eof()

        r = await wow_login_messages.version2.expect_client_opcode(reader, wow_login_messages.version2.CMD_XFER_CANCEL)
        self.assertIsNotNone(r)
        self.assertTrue(reader.at_eof())
        written = bytearray(len(data))
        r.write(written)
        self.assertEqual(data, written)


