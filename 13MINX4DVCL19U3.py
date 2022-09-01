import amino
from .utils import configs
from tabulate import tabulate
from asyncio import gather, create_task, get_event_loop

client = amino.AsyncClient()

async def auth():
	while True:
		try:
			email = input("[Email]]::: ")
			password = input("[Password]]::: ")
			await client.login(email=email, password=password)
			break
		except Exception as e:
			print(e)

async def communities():
	while True:
		try:
			clients = await client.sub_clients(start=0, size=100)
			for x, name in enumerate(clients.name, 1):
				print(f"[{x}]:[{name}]")
			return clients.comId[int(input("[Select the community]::: ")) - 1]
		except Exception as e:
			print(e)


async def advertise_in_global(
		sub_client: amino.AsyncSubClient, message: str):
	while True:
		try:
			online_users = await sub_client.get_online_users(size=100).userId
			await asyncio.gather(*[
				asyncio.create_task(client.start_chat(users, message)
			) for _ in range(50)])
		except Exception as e:
			print(e)

async def advertise_in_community(
		sub_client: amino.AsyncSubClient, message: str):
	while True:
		try:
			online_users = await sub_client.get_online_users(size=100).userId
			await asyncio.gather(*[
				asyncio.create_task(sub_client.start_chat(online_users, message)
			) for _ in range(50)])
		except Exception as e:
			print(e)

async def advertise_to_user(
		sub_client: amino.AsyncSubClient, message: str):
	user_id = await client.get_from_code(input("[User link]::: ")).objectId
	with open("accounts.txt", "r") as accounts:
		for account in accounts:
			try:
				data = accounts.split(":")
				email = data[0]
				password = data[1]
				await client.login(email=email, password=password)
				print(f"[{email}][is advertising to]::: [{user_id}]")
				await asyncio.gather(*[
					asyncio.create_task(sub_client.start_chat(user_id, message)
				) for _ in range(50)])
			except Exception as e:
				print(e)

async def start():
	print(configs.LOGO)
	await auth()
	com_id = await communities()
	sub_client = amino.AsyncSubClient(comId=com_id, profile=client.profile)
	print(tabulate(configs.MAIN_MENU, tablefmt="rst"))
	select = int(input("[Select]::: "))
	message = input("[Message]::: ")
	if select == 1:
		await advertise_in_global(sub_client, message)
	elif select == 2:
		await advertise_in_community(sub_client, message)
	elif select == 3:
		await advertise_to_user(sub_client, message)

get_event_loop().run_until_complete(start())
