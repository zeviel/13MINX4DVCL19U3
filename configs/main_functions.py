import asyncio
import pyfiglet
import aminofix.asyncfix
from . import menu_configs
from tabulate import tabulate
client = aminofix.asyncfix.Client()

		# -- login and other functions --

# login


async def auth():
    while True:
        try:
            email = input("Email >> ")
            password = input("Password >> ")
            await client.login(email=email, password=password)
            return False
        except Exception as e:
            print(e)

# get joined communities list


async def communities():
    try:
        clients = await client.sub_clients(start=0, size=100)
        for x, name in enumerate(clients.name, 1):
            print(f"{x}.{name}")
        while True:
            com_Id = clients.comId[int(input("Select the community >> ")) - 1]
            return com_Id
    except ValueError:
        communities()
    except Exception as e:
        print(e)

        # -- login and other functions --

        # -- community, global advertise --

default_list = []


def advertise(user: str):
    users_list = []
    for user_Id in user.profile.userId:
        users_list.append(user_Id)
    return users_list

# community advertise proccess


async def community_advertise_process(message: str):
    sub_client = aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    while True:
        try:
            print(">> Advertising...")
            online_users = await sub_client.get_online_users(size=100)
            users = advertise(online_users)
            for i in default_list:
                if i in users:
                    users.remove(i)
            await asyncio.gather(*[asyncio.create_task(sub_client.start_chat(users, message)) for _ in range(50)])
        except aminofix.asyncfix.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired...")
            verification_link = e.args[0]["url"]
            print(f"Verification Link >> {verification_link}")
            verification = input("Waiting for verification >> ")
        except Exception as e:
            print(e)

# global advertise proccess


async def global_advertise_process(message: str):
    sub_client = aminofix.asyncfix.SubClient(comId=await communities(), profile=client.profile)
    while True:
        try:
            print(">> Advertising...")
            online_users = await sub_client.get_online_users(size=100)
            users = advertise(online_users)
            for i in default_list:
                if i in users:
                    users.remove(i)
            await asyncio.gather(*[asyncio.create_task(client.start_chat(users, message)) for _ in range(50)])
        except aminofix.asyncfix.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired...")
            verification_link = e.args[0]["url"]
            print(f"Verification Link >> {verification_link}")
            verification = input("Waiting for verification >> ")
        except Exception as e:
            print(e)

# community advertise


async def community_advertise():
    await auth()
    await community_advertise_process(message=input("Message >> "))

# global advertise


async def global_advertise():
    await auth()
    await global_advertise_process(message=input("Message >> "))

    # -- community, global advertise --

    # -- advertise to selected user --

# using one account


async def using_one_account(message: str):
    await auth()
    link_Info = await client.get_from_code(input("User Link >> "))
    user_Id = link_Info.objectId
    com_Id = link_Info.comId
    sub_client = aminofix.asyncfix.SubClient(
        comId=com_Id, profile=client.profile)
    while True:
        try:
            print(">> Advertising To Selected User...")
            await asyncio.gather(*[asyncio.create_task(sub_client.start_chat([client.userId, user_Id], message)) for _ in range(50)])
        except aminofix.asyncfix.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired...")
            verification_link = e.args[0]["url"]
            print(f"Verification Link >> {verification_link}")
            verification = input("Waiting for verification >> ")
        except Exception as e:
            print(e)

# using multiple accounts


async def using_multiple_accounts(message: str):
    link_Info = await client.get_from_code(input("User Link >> "))
    user_Id = link_Info.objectId
    com_Id = link_Info.comId
    sub_client = aminofix.asyncfix.SubClient(
        comId=com_Id, profile=client.profile)
    accounts = open("emails.txt", "r")
    for line in accounts:
        try:
            email = line.split(":")[0]
            password = line.split(":")[1]
            await client.login(email=email, password=password)
            print(f">> {email} Logged In...")
            print(">> Advertising To Selected User...")
            await asyncio.gather(*[asyncio.create_task(sub_client.start_chat(user_Id, message)) for _ in range(50)])
        except aminofix.asyncfix.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired...")
            verification_link = e.args[0]["url"]
            print(f"Verification Link >> {verification_link}")
            verification = input("Waiting for verification >> ")
        except Exception as e:
            print(e)

        # -- advertise to selected user --

        # -- main proccess --

# advertise to selected user


async def advertise_to_selected_user():
    print(tabulate(menu_configs.additional_menu, tablefmt="rst"))
    select = input("Select >> ")
    if select == "1":
        await using_one_account(message=input("Message >> "))
    elif select == "2":
        await using_multiple_accounts(message=input("Message >> "))

# main function with community, global and other advertise types


async def main():
    print(tabulate(menu_configs.main_menu, tablefmt="rst"))
    select = input("Select >> ")
    if select == "1":
        await global_advertise()
    elif select == "2":
        await community_advertise()
    elif select == "3":
        await advertise_to_selected_user()

        # -- main proccess --

# End...
