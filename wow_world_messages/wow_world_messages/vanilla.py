import asyncio
import dataclasses
import enum
import struct
import typing

import wow_srp


@dataclasses.dataclass
class SMSG_AUTH_CHALLENGE:
    server_seed: int

    @staticmethod
    async def read(reader: asyncio.StreamReader):
        server_seed = int.from_bytes(await reader.readexactly(4), "little")

        return SMSG_AUTH_CHALLENGE(server_seed)

    def write_unencrypted(self, writer: asyncio.StreamWriter):
        header = bytearray(4 + 4)
        # Header
        size = 4 + 2
        struct.pack_into(">H", header, 0, size)
        opcode = 0x01EC
        struct.pack_into("<H", header, 2, opcode)

        fmt = "<"
        data = []

        # server_seed: u32
        fmt += "I"
        data.append(self.server_seed)

        struct.pack_into(fmt, header, 4, *data)
        print(header)
        writer.write(header)


@dataclasses.dataclass
class CMSG_AUTH_SESSION:
    build: int
    server_id: int
    username: str
    client_seed: int
    client_proof: list[int]
    decompressed_addon_info_size: int
    addon_info: list[int]

    @staticmethod
    async def read(reader: asyncio.StreamReader, body_size: int):
        build = int.from_bytes(await reader.readexactly(4), "little")

        server_id = int.from_bytes(await reader.readexactly(4), "little")

        username = (await reader.readuntil(b"\x00")).decode("utf-8").rstrip("\x00")

        client_seed = int.from_bytes(await reader.readexactly(4), "little")

        client_proof = []
        for _ in range(0, 20):
            client_proof.append(int.from_bytes(await reader.readexactly(1), "little"))

        decompressed_addon_info_size = int.from_bytes(
            await reader.readexactly(4), "little"
        )

        current_size = 4 + 4 + 1 + len(username) + 4 + 20 + 4

        addon_info = []
        for _ in range(current_size, body_size):
            addon_info.append(int.from_bytes(await reader.readexactly(1), "little"))

        return CMSG_AUTH_SESSION(
            build,
            server_id,
            username,
            client_seed,
            client_proof,
            decompressed_addon_info_size,
            addon_info,
        )

    def write(self, writer: asyncio.StreamWriter):
        raise Exception("unimpl")


class WorldResult(enum.Enum):
    RESPONSE_SUCCESS = 0x00
    RESPONSE_FAILURE = 0x01
    RESPONSE_CANCELLED = 0x02
    RESPONSE_DISCONNECTED = 0x03
    RESPONSE_FAILED_TO_CONNECT = 0x04
    RESPONSE_CONNECTED = 0x05
    RESPONSE_VERSION_MISMATCH = 0x06
    CSTATUS_CONNECTING = 0x07
    CSTATUS_NEGOTIATING_SECURITY = 0x08
    CSTATUS_NEGOTIATION_COMPLETE = 0x09
    CSTATUS_NEGOTIATION_FAILED = 0x0A
    CSTATUS_AUTHENTICATING = 0x0B
    AUTH_OK = 0x0C
    AUTH_FAILED = 0x0D
    AUTH_REJECT = 0x0E
    AUTH_BAD_SERVER_PROOF = 0x0F
    AUTH_UNAVAILABLE = 0x10
    AUTH_SYSTEM_ERROR = 0x11
    AUTH_BILLING_ERROR = 0x12
    AUTH_BILLING_EXPIRED = 0x13
    AUTH_VERSION_MISMATCH = 0x14
    AUTH_UNKNOWN_ACCOUNT = 0x15
    AUTH_INCORRECT_PASSWORD = 0x16
    AUTH_SESSION_EXPIRED = 0x17
    AUTH_SERVER_SHUTTING_DOWN = 0x18
    AUTH_ALREADY_LOGGING_IN = 0x19
    AUTH_LOGIN_SERVER_NOT_FOUND = 0x1A
    AUTH_WAIT_QUEUE = 0x1B
    AUTH_BANNED = 0x1C
    AUTH_ALREADY_ONLINE = 0x1D
    AUTH_NO_TIME = 0x1E
    AUTH_DB_BUSY = 0x1F
    AUTH_SUSPENDED = 0x20
    AUTH_PARENTAL_CONTROL = 0x21
    REALM_LIST_IN_PROGRESS = 0x22
    REALM_LIST_SUCCESS = 0x23
    REALM_LIST_FAILED = 0x24
    REALM_LIST_INVALID = 0x25
    REALM_LIST_REALM_NOT_FOUND = 0x26
    ACCOUNT_CREATE_IN_PROGRESS = 0x27
    ACCOUNT_CREATE_SUCCESS = 0x28
    ACCOUNT_CREATE_FAILED = 0x29
    CHAR_LIST_RETRIEVING = 0x2A
    CHAR_LIST_RETRIEVED = 0x2B
    CHAR_LIST_FAILED = 0x2C
    CHAR_CREATE_IN_PROGRESS = 0x2D
    CHAR_CREATE_SUCCESS = 0x2E
    CHAR_CREATE_ERROR = 0x2F
    CHAR_CREATE_FAILED = 0x30
    CHAR_CREATE_NAME_IN_USE = 0x31
    CHAR_CREATE_DISABLED = 0x32
    CHAR_CREATE_PVP_TEAMS_VIOLATION = 0x33
    CHAR_CREATE_SERVER_LIMIT = 0x34
    CHAR_CREATE_ACCOUNT_LIMIT = 0x35
    CHAR_CREATE_SERVER_QUEUE = 0x36
    CHAR_CREATE_ONLY_EXISTING = 0x37
    CHAR_DELETE_IN_PROGRESS = 0x38
    CHAR_DELETE_SUCCESS = 0x39
    CHAR_DELETE_FAILED = 0x3A
    CHAR_DELETE_FAILED_LOCKED_FOR_TRANSFER = 0x3B
    CHAR_LOGIN_IN_PROGRESS = 0x3C
    CHAR_LOGIN_SUCCESS = 0x3D
    CHAR_LOGIN_NO_WORLD = 0x3E
    CHAR_LOGIN_DUPLICATE_CHARACTER = 0x3F
    CHAR_LOGIN_NO_INSTANCES = 0x40
    CHAR_LOGIN_FAILED = 0x41
    CHAR_LOGIN_DISABLED = 0x42
    CHAR_LOGIN_NO_CHARACTER = 0x43
    CHAR_LOGIN_LOCKED_FOR_TRANSFER = 0x44
    CHAR_NAME_NO_NAME = 0x45
    CHAR_NAME_TOO_SHORT = 0x46
    CHAR_NAME_TOO_LONG = 0x47
    CHAR_NAME_ONLY_LETTERS = 0x48
    CHAR_NAME_MIXED_LANGUAGES = 0x49
    CHAR_NAME_PROFANE = 0x4A
    CHAR_NAME_RESERVED = 0x4B
    CHAR_NAME_INVALID_APOSTROPHE = 0x4C
    CHAR_NAME_MULTIPLE_APOSTROPHES = 0x4D
    CHAR_NAME_THREE_CONSECUTIVE = 0x4E
    CHAR_NAME_INVALID_SPACE = 0x4F
    CHAR_NAME_SUCCESS = 0x50
    CHAR_NAME_FAILURE = 0x51


@dataclasses.dataclass
class SMSG_AUTH_RESPONSE:
    result: WorldResult
    billing_time: typing.Optional[int] = None
    billing_flags: typing.Optional[int] = None
    billing_rested: typing.Optional[int] = None
    queue_position: typing.Optional[int] = None

    @staticmethod
    async def read(reader: asyncio.StreamReader, body_size: int):
        billing_time = None
        billing_flags = None
        billing_rested = None
        queue_position = None

        result = WorldResult(int.from_bytes(await reader.readexactly(1), "little"))

        if result == WorldResult.AUTH_OK:
            billing_time = int.from_bytes(await reader.readexactly(4), "little")

            billing_flags = int.from_bytes(await reader.readexactly(1), "little")

            billing_rested = int.from_bytes(await reader.readexactly(4), "little")
        elif result == WorldResult.AUTH_WAIT_QUEUE:
            queue_position = int.from_bytes(await reader.readexactly(4), "little")

        return SMSG_AUTH_RESPONSE(
            result=result,
            billing_time=billing_time,
            billing_flags=billing_flags,
            billing_rested=billing_rested,
            queue_position=queue_position,
        )

    def write_encrypted(
        self,
        writer: asyncio.StreamWriter,
        header_crypto: wow_srp.vanilla_header.HeaderCrypto,
    ):
        size = self._size() + 2
        opcode = 0x01EE
        data = bytes(header_crypto.encrypt_server_header(size, opcode))
        header = bytearray(4 + self._size())
        # Header
        struct.pack_into("<4s", header, 0, data)

        fmt = "<"
        data = []

        fmt += "B"
        data.append(self.result.value)

        if self.result == WorldResult.AUTH_OK:
            fmt += "I"
            data.append(self.billing_time)

            fmt += "B"
            data.append(self.billing_flags)

            fmt += "I"
            data.append(self.billing_rested)
        elif self.result == WorldResult.AUTH_WAIT_QUEUE:
            fmt += "I"
            data.append(self.queue_position)

        struct.pack_into(fmt, header, 4, *data)
        print(header)
        writer.write(header)

    def _size(self) -> int:
        size = 0

        size += 1

        if self.result == WorldResult.AUTH_OK:
            size += 4
            size += 1
            size += 4
        elif self.result == WorldResult.AUTH_WAIT_QUEUE:
            size += 4

        return size


@dataclasses.dataclass
class CMSG_CHAR_ENUM:
    pass

    @staticmethod
    async def read(reader: asyncio.StreamReader, body_size: int):
        return CMSG_CHAR_ENUM()

    def write_encrypted(
        self,
        writer: asyncio.StreamWriter,
        header_crypto: wow_srp.vanilla_header.HeaderCrypto,
    ):
        size = 2
        opcode = 0x0037
        data = bytes(header_crypto.encrypt_server_header(size, opcode))

        data = struct.pack("<4s", data)

        print(data)
        writer.write(data)
