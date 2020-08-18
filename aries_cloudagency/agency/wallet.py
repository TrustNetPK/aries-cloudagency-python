from aiohttp import web

from .storage import AgencyStorage
from ..wallet.indy import IndyWallet
from ..utils.classloader import ClassLoader
from ..wallet.base import BaseWallet
import threading
import logging
import json
import asyncio
import time

# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
open_wallets = {}  # in-memory open wallets
wallet_class = 'aries_cloudagency.wallet.indy.IndyWallet'
agency_storage = AgencyStorage()



# storage_config_json = json.dumps({"url": "localhost:5432"})
# storage_creds_json = json.dumps(
#         {
#             "account": "postgres",
#             "password": "123",
#             "admin_account": "postgres",
#             "admin_password": "123",
#         },
#     )


async def wallet_create_thread(wallet_cfg):
    wt: IndyWallet = ClassLoader.load_class(wallet_class)(wallet_cfg)
    try:
        # time.sleep(1)
        await wt.open()
        public_did = await wt.create_public_did(seed=wallet_cfg["seed"])
        open_wallets[wallet_cfg["name"]] = wt
        await agency_storage.store_wallet(wallet_cfg["name"], wallet_cfg["key"], public_did[1], public_did[0])
        # time.sleep(1)

        # indyWallet = IndyWallet({
        #     "auto_create": True,
        #     "auto_remove": False,
        #     "name": wallet_cfg["name"],
        #     "key": wallet_cfg["key"],
        #     "storage_type": "postgres_storage",
        #     "storage_config": storage_config_json,
        #     "storage_creds": storage_creds_json,
        #     "key_derivation_method": "RAW",  # much slower tests with argon-hashed keys
        # })
        # await indyWallet.create()
    except Exception as ex:
        print("Error!")
        print(ex)

def start_background_loop(loop: asyncio.AbstractEventLoop, wallet_cfg) -> None:
    asyncio.set_event_loop(loop)
    loop.run_until_complete(wallet_create_thread(wallet_cfg))

# async def create(request):
#     wallet_cfg = {}
#     params = await request.json()
#     wallet_cfg["name"] = params['wallet_name']
#     wallet_cfg["seed"] = params['seed']
#     wallet_cfg["key"] = await IndyWallet.generate_wallet_key()
#     try:
#         loop = asyncio.new_event_loop()
#         t = threading.Thread(target=start_background_loop, args=(loop,wallet_cfg,), daemon=False)
#         t.start()
#         resp = {"wallet_secret": wallet_cfg["key"]}
#         return web.json_response(resp)
#     except Exception as ex:
#         print("Error!")
#         print(ex)

async def create(request):
    wallet_cfg = {}
    params = await request.json()
    wallet_cfg["name"] = params['wallet_name']
    wallet_cfg["seed"] = params['seed']
    wallet_cfg["key"] = await IndyWallet.generate_wallet_key()
    try:
        wt: IndyWallet = ClassLoader.load_class(wallet_class)(wallet_cfg)
        await wt.open()
        public_did = await wt.create_public_did(seed=wallet_cfg["seed"])
        open_wallets[wallet_cfg["name"]] = wt
        await agency_storage.store_wallet(wallet_cfg["name"], wallet_cfg["key"], public_did[1], public_did[0])
        resp = {"wallet_secret": wallet_cfg["key"]}
        return web.json_response(resp)
    except Exception as ex:
        print("Error!")
        print(ex)

async def open(name, key):
    wallet_cfg = {"name": name, "key": key}
    wt = ClassLoader.load_class(wallet_class)(wallet_cfg)
    try:
        await wt.open()
        open_wallets[name] = wt
        return wt
    except Exception as ex:
        print(ex)


async def close(name, key):
    wallet_cfg = {"name": name, "key": key}
    wt = ClassLoader.load_class(wallet_class)(wallet_cfg)
    try:
        await wt.close()
    except Exception as ex:
        print(ex)


async def get(name, key):
    agency_storage = AgencyStorage()
    wallet_info = await agency_storage.get_wallet(name, key)
    if wallet_info is not None:
        wlt = open_wallets.get(name)
        if wlt:
            return wlt
        else:
            return await open(name, key)
    else:
        return None
