import asyncio

import wow_srp

import wow_login_messages.wow_login_messages.util as login_util
import wow_login_messages.wow_login_messages.version3 as login


async def login_path(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    request: login.CMD_AUTH_LOGON_CHALLENGE_Client,
):
    server = wow_srp.SrpVerifier.from_username_and_password(
        request.account_name, request.account_name
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
                "localhost",
                login.Population.RED_FULL,
                0,
                login.RealmCategory.ONE,
                0,
            )
        ]
    )
    print(response)
    response.write(writer)


async def client_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    request = await login_util.expect_login_or_reconnect(reader)
    match request:
        case None:
            print("invalid starting opcode")
            return
        case login.CMD_AUTH_LOGON_CHALLENGE_Client():
            print(request)
            await login_path(reader, writer, request)


async def run_server():
    server = await asyncio.start_server(client_connection, "localhost", 3724)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())
