import asyncio

import wow_srp

import wow_login_messages.version3 as login
import wow_world_messages.vanilla as world
from wow_world_messages.vanilla import (
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
    print(account_name)
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

    request = await login.read_client_opcode(reader)
    print(request)
    server, proof = server.into_server(request.client_public_key, request.client_proof)
    if server is None:
        print("invalid password")
        raise Exception("invalid password")

    session_keys[account_name] = server

    response = login.CMD_AUTH_LOGON_PROOF_Server(login.LoginResult.SUCCESS, proof, 0)
    response.write(writer)

    opcode = await login.read_client_opcode(reader)
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
                "127.0.0.1:8085",
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
    print("connect")
    try:
        request = await login.read_client_opcode(reader)
        match request:
            case login.CMD_AUTH_LOGON_CHALLENGE_Client():
                print(request)
                await login_path(reader, writer, request)
            case _:
                print("invalid starting opcode")
                return
    except Exception as e:
        print(e)
        exit(1)


async def world_path(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    seed = wow_srp.VanillaProofSeed()

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

    world.SMSG_AUTH_RESPONSE(world.WorldResult.AUTH_OK, 0, 0, 0).write_encrypted_server(
        writer, crypto
    )

    opcode = await read_client_opcodes_encrypted(reader, crypto)
    print(opcode)

    c = world.SMSG_CHAR_ENUM(
        characters=[
            world.Character(
                1,
                "TestChar",
                world.Race.HUMAN,
                world.Class.WARRIOR,
                world.Gender.MALE,
                0,
                0,
                0,
                0,
                0,
                1,
                world.Area.NORTHSHIRE_ABBEY,
                world.Map.EASTERN_KINGDOMS,
                world.Vector3d(0.0, 0.0, 0.0),
                0,
                world.CharacterFlags.NONE,
                False,
                0,
                0,
                world.CreatureFamily.NONE,
                [
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                    world.CharacterGear(0, world.InventoryType.NON_EQUIP),
                ],
            )
        ]
    )
    print(c)
    c.write_encrypted_server(writer, crypto)

    opcode = await read_client_opcodes_encrypted(reader, crypto)
    print(opcode)

    match opcode:
        case world.CMSG_PLAYER_LOGIN(guid=guid):
            print(f"Logging into {guid}")

            position = world.Vector3d(
                x=-8949.95,
                y=-132.493,
                z=83.5312,
            )

            world.SMSG_LOGIN_VERIFY_WORLD(
                map=world.Map.EASTERN_KINGDOMS,
                position=position,
                orientation=0.0,
            ).write_encrypted_server(writer, crypto)

            world.SMSG_TUTORIAL_FLAGS(
                tutorial_data=[
                    0xFF, 0xFF, 0xFF, 0xFF,
                    0xFF, 0xFF, 0xFF, 0xFF,
                ]
            ).write_encrypted_server(writer, crypto)

            mask = world.UpdateMask(fields={
                world.UpdateMaskValue.OBJECT_GUID: guid,
                world.UpdateMaskValue.OBJECT_SCALE_X: 1.0,
                world.UpdateMaskValue.OBJECT_TYPE: 25,
                world.UpdateMaskValue.UNIT_BYTES_0: 0x01010101,
                world.UpdateMaskValue.UNIT_DISPLAYID: 50,
                world.UpdateMaskValue.UNIT_FACTIONTEMPLATE: 1,
                world.UpdateMaskValue.UNIT_HEALTH: 100,
                world.UpdateMaskValue.UNIT_LEVEL: 1,
                world.UpdateMaskValue.UNIT_NATIVEDISPLAYID: 50,
            })

            world.SMSG_UPDATE_OBJECT(
                has_transport=0,
                objects=[
                    world.Object(
                        update_type=world.UpdateType.CREATE_OBJECT2,
                        guid3=guid,
                        object_type=world.ObjectType.PLAYER,
                        movement2=world.MovementBlock(
                            update_flag=world.UpdateFlag.SELF | world.UpdateFlag.ALL | world.UpdateFlag.LIVING,
                            flags=world.MovementFlags.NONE,
                            timestamp=0,
                            living_position=position,
                            living_orientation=0.0,
                            fall_time=0.0,
                            walking_speed=1.0,
                            running_speed=70.0,
                            backwards_running_speed=4.5,
                            swimming_speed=0.0,
                            backwards_swimming_speed=0.0,
                            turn_rate=3.1415,
                            unknown1=0,
                        ),
                        mask2=mask,
                    )
                ]
            ).write_encrypted_server(writer, crypto)


async def world_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        await world_path(reader, writer)
    except Exception as e:
        print(e)
        exit()


async def run_server():
    login_server = await asyncio.start_server(login_connection, "127.0.0.1", 3724)
    world_server = await asyncio.start_server(world_connection, "127.0.0.1", 8085)
    async with login_server:
        await asyncio.gather(login_server.serve_forever(), world_server.serve_forever())


asyncio.run(run_server())
