import pickledb
import json
from pathlib import Path


class AgencyStorage:

    def __init__(self):
        home = str(Path.home())
        self.wallet_db = pickledb.load(home+'/.indy_client/wallets.db', True)
        self.recipient_db = pickledb.load(home+'/.indy_client/recipients.db', True)

    async def store_wallet(self, wallet_name, wallet_secret, ver_key, did):
        wallet_info = {"wallet_secret": wallet_secret, "ver_key": ver_key, "did": did}
        self.wallet_db.set(wallet_name, json.dumps(wallet_info))
        self.wallet_db.dump()

    async def get_wallet(self, wallet_name, wallet_secret):
        wallet_info = self.wallet_db.get(wallet_name)
        if wallet_info:
            wallet = json.loads(str(wallet_info))
            if wallet['wallet_secret'] == wallet_secret:
                return wallet_info
            else:
                return None
        return None

    async def get_wallet_without_secret(self, wallet_name):
        wallet_info = self.wallet_db.get(wallet_name)
        if wallet_info:
            wallet = json.loads(str(wallet_info))
            return wallet
        else:
            return None

    async def store_recipient(self, wallet_name, ver_key, did):
        recipient_info = {"wallet_name": wallet_name, "ver_key": ver_key, "did": did}
        self.recipient_db.set(ver_key, json.dumps(recipient_info))
        self.recipient_db.dump()

    async def get_recipient(self, ver_key):
        recipient_info = self.recipient_db.get(ver_key)
        if recipient_info:
            recipient = json.loads(str(recipient_info))
            return recipient
        else:
            return None
