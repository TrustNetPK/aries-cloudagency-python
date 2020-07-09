from aiohttp import web

from .storage import AgencyStorage
from ..wallet.indy import IndyWallet
from ..utils.classloader import ClassLoader
from ..wallet.base import BaseWallet

open_wallets = {}  # in-memory open wallets
wallet_class = 'aries_cloudagency.wallet.indy.IndyWallet'


async def create(request):
    wallet_cfg = {}
    params = await request.json()
    wallet_cfg["name"] = params['wallet_name']
    provided_seed = params['seed']
    wallet_cfg["key"] = await IndyWallet.generate_wallet_key()
    wt: BaseWallet = ClassLoader.load_class(wallet_class)(wallet_cfg)
    try:
        await wt.open()
        public_did = await wt.create_public_did(seed=provided_seed)
        open_wallets[wallet_cfg["name"]] = wt
        resp = {"did": public_did[0], "ver_key": public_did[1], "type": public_did[2],
                "wallet_secret": wallet_cfg["key"]}
        agency_storage = AgencyStorage()
        await agency_storage.store_wallet(wallet_cfg["name"], wallet_cfg["key"], public_did[1], public_did[0])
        return web.json_response(resp)
    except Exception as ex:
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
