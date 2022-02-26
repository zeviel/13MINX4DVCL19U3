import amino
from . import menu_configs
from tabulate import tabulate
client = amino.AsyncClient()

		# -- login and other functions --

# login
async def auth():
    while True:
        try:
            email = input("-- Email::: ")
            password = input("-- Password::: ")
            await client.login(email=email, password=password)
            return False
        except Exception as e:
            print(e)

async def communities():
	while True:
		try:
			clients = await client.sub_clients(start=0, size=100)
			for x, name in enumerate(clients.name, 1):
				print(f"-- {x}:{name}")
			com_id = clients.comId[int(input("-- Select the community::: ")) - 1]
			return com_id
		except Exception as e:
			print(e)

        # -- login and other functions --


        # -- community, global advertise --

# community advertise process
async def community_advertise_process(sub_client: amino.AsyncSubClient, message: str):
    while True:
        try:
            print("-- Advertising...")
            online_users = await sub_client.get_online_users(size=100).profile.userId
            await asyncio.gather(*[asyncio.create_task(sub_client.start_chat(online_users, message)) for _ in range(50)])
        except amino.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired::: {e.args[0]['url']}") 
            verification = input("-- Press enter after verification...")
        except Exception as e:
            print(e)

# global advertise proccess


async def global_advertise_process(sub_client: amino.AsyncSubClient, message: str):
    while True:
        try:
            print("-- Advertising...")
            online_users = await sub_client.get_online_users(size=100).profile.userId
            await asyncio.gather(*[asyncio.create_task(client.start_chat(users, message)) for _ in range(50)])
        except amino.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired::: {e.args[0]['url']}") 
            verification = input("-- Press enter after verification...")
        except Exception as e:
            print(e)

    # -- advertise to selected user --

# using one account


async def using_one_account(sub_client: amino.AsyncSubClient, message: str):
    user_id = await client.get_from_code(input("-- User link::: ")).objectId
    while True:
        try:
            print(">> Advertising To Selected User...")
            await asyncio.gather(*[asyncio.create_task(sub_client.start_chat([client.userId, user_Id], message)) for _ in range(50)])
        except amino.lib.util.exceptions.VerificationRequired as e:
            print(">> Error - VerificationRequired::: {e.args[0]['url']}") 
            verification = input("-- Press enter after verification...")
        except Exception as e:
            print(e)

# using multiple accounts


async def using_multiple_accounts(sub_client: amino.AsyncSubClient, message: str):
    user_id = await client.get_from_code(input("-- User link::: ")).objectId
    with open ("emails.txt", "r") as accounts:
    	for line in accounts:
    		try:
    			email, password = line.split(":")[0], line.split(":")[1]
    			await client.login(email=email, password=password)
    			print(f"-- {email} Logged in and started advertising to selected user...")
    			await asyncio.gather(*[asyncio.create_task(sub_client.start_chat(user_id, message)) for _ in range(50)])
    		except amino.lib.util.exceptions.VerificationRequired as e:
    		      print(">> Error - VerificationRequired::: {e.args[0]['url']}") 
    		      verification = input("-- Press enter after verification...")
    		except Exception as e:
    			print(e)

        # -- advertise to selected user --


        # -- main proccess --

# advertise to selected user
async def advertise_to_selected_user(sub_client: amino.AsyncSubClient, message: str):
    print(tabulate(menu_configs.additional_menu, tablefmt="rst"))
    select = int(input("-- Select::: "))
    if select == 1: await using_one_account(sub_client=sub_client, message=message)
    elif select == 2: await using_multiple_accounts(sub_client=sub_client, message=message)

# main function with community, global and other advertise types
async def main():
	await auth()
	sub_client = amino.AsyncSubClient(comId=await communities(), profile=client.profile)
	print(tabulate(menu_configs.main_menu, tablefmt="rst"))
	select = int(input("-- Select::: "))
	message = input("-- Message::: ")
	if select == 1: global_advertise_process(sub_client=sub_client, message=message)
	elif select == 2: await community_advertise_process(sub_client=sub_client, message=message)
	elif select == 3: await advertise_to_selected_user(sub_client=sub_client, message=message)
    
        # -- main proccess --
