import pickledb
import json
from pathlib import Path


class AgencyStorage:

    wallet_db = None
    recipient_db = None
    # home = None

    def __init__(self):
        if AgencyStorage.wallet_db == None and AgencyStorage.recipient_db == None:
            # AgencyStorage.home = str(Path.home())
            AgencyStorage.wallet_db = {}
            AgencyStorage.recipient_db = {}

    async def store_wallet(self, wallet_name, wallet_secret, ver_key, did):
        wallet_info = {"wallet_secret": wallet_secret, "ver_key": ver_key, "did": did}
        AgencyStorage.wallet_db[wallet_name] = json.dumps(wallet_info)

    async def get_wallet(self, wallet_name, wallet_secret):
        wallet_info = AgencyStorage.wallet_db[wallet_name]
        if wallet_info:
            wallet = json.loads(str(wallet_info))
            if wallet['wallet_secret'] == wallet_secret:
                return wallet_info
            else:
                return None
        return None

    async def get_wallet_without_secret(self, wallet_name):
        wallet_info = AgencyStorage.wallet_db[wallet_name]
        if wallet_info:
            wallet = json.loads(str(wallet_info))
            return wallet
        else:
            return None

    async def store_recipient(self, wallet_name, ver_key, did):
        recipient_info = {"wallet_name": wallet_name, "ver_key": ver_key, "did": did}
        AgencyStorage.recipient_db[ver_key] = json.dumps(recipient_info)

    async def get_recipient(self, ver_key):
        recipient_info = AgencyStorage.recipient_db[ver_key]
        if recipient_info:
            recipient = json.loads(str(recipient_info))
            return recipient
        else:
            return None
