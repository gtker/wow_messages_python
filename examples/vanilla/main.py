import asyncio

import wow_srp

import wow_login_messages.wow_login_messages.util as login_util
import wow_login_messages.wow_login_messages.version3 as login
import wow_world_messages.wow_world_messages.vanilla as world
from wow_world_messages.wow_world_messages.util import (
    expect_client_opcode_unencrypted,
    read_client_opcodes_encrypted,
)

session_keys = {}


async def login_path(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    request: login.CMD_AUTH_LOGON_CHALLENGE_Client,
):
    account_name = request.account_name
    server = wow_srp.SrpVerifier.from_username_and_password(
        account_name, request.account_name
    ).into_proof()

    response = login.CMD_AUTH_LOGON_CHALLENGE_Server(
        login.LoginResult.SUCCESS,
        server.server_public_key(),
        [wow_srp.generator()],
        wow_srp.large_safe_prime(),
        server.salt(),
        [0] * 16,
        login.SecurityFlag(0),
        None,
        None,
    )
    print(response)
    response.write(writer)

    request = await login_util.read_opcode_server(reader)
    print(request)
    server, proof = server.into_server(request.client_public_key, request.client_proof)
    if server is None:
        print("invalid password")
        raise Exception("invalid password")

    session_keys[account_name] = server

    response = login.CMD_AUTH_LOGON_PROOF_Server(login.LoginResult.SUCCESS, proof, 0)
    response.write(writer)

    opcode = await login_util.read_opcode_server(reader)
    match opcode:
        case login.CMD_REALM_LIST_Client():
            pass
        case v:
            raise Exception(f"{v}")

    response = login.CMD_REALM_LIST_Server(
        [
            login.Realm(
                login.RealmType.PLAYER_VS_ENVIRONMENT,
                login.RealmFlag.NONE,
                "A",
                "localhost:8085",
                400.0,
                0,
                login.RealmCategory.ONE,
                0,
            )
        ]
    )
    print(response)
    response.write(writer)


async def login_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        request = await login_util.expect_login_or_reconnect(reader)
        match request:
            case None:
                print("invalid starting opcode")
                return
            case login.CMD_AUTH_LOGON_CHALLENGE_Client():
                print(request)
                await login_path(reader, writer, request)
    except Exception as e:
        print(e)
        exit(1)


async def world_path(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    seed = wow_srp.vanilla_header.ProofSeed()

    world.SMSG_AUTH_CHALLENGE(seed.seed()).write_unencrypted(writer)

    opcode = await expect_client_opcode_unencrypted(reader, world.CMSG_AUTH_SESSION)
    if opcode is None:
        raise Exception("incorrect opcode")
    print(opcode)

    if opcode.username not in session_keys:
        raise Exception("username not in session keys")

    server = session_keys[opcode.username]
    crypto = seed.into_server_header_crypto(
        opcode.username, server.session_key(), opcode.client_proof, opcode.client_seed
    )

    world.SMSG_AUTH_RESPONSE(world.WorldResult.AUTH_OK, 0, 0, 0).write_encrypted(
        writer, crypto
    )

    opcode = await read_client_opcodes_encrypted(reader, crypto)
    print(opcode)


async def world_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        await world_path(reader, writer)
    except Exception as e:
        print(e)
        exit()


async def run_server():
    login_server = await asyncio.start_server(login_connection, "localhost", 3724)
    world_server = await asyncio.start_server(world_connection, "localhost", 8085)
    async with login_server:
        await asyncio.gather(login_server.serve_forever(), world_server.serve_forever())


asyncio.run(run_server())
