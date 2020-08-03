import asyncio

import os
from aries_cloudagency.config.default_context import DefaultContextBuilder
from aries_cloudagency.core.conductor import Conductor

contextBuilder = DefaultContextBuilder()


def str_to_bool(s):
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        raise ValueError


admin_insecure_mode = str_to_bool(os.getenv("admin_insecure_mode", "False").lower())
admin_api_key = os.getenv("admin_api_key", "secret")
admin_port = os.getenv("admin_port", "2500")
agency_endpoint = os.getenv("agency_endpoint", "http://0.0.0.0")
inbound_port = os.getenv("inbound_port", "7500")
genesis_url = os.getenv("genesis_url", "http://greenlight.bcovrin.vonx.io/genesis")


async def start():
    # Build Context
    contextBuilder.settings.set_default("admin.enabled", True)
    if admin_insecure_mode:
        contextBuilder.settings.set_default("admin.admin_insecure_mode", admin_insecure_mode)
    else:
        contextBuilder.settings.set_default("admin.admin_api_key", admin_api_key)
    contextBuilder.settings.set_default("admin.host", "0.0.0.0")
    contextBuilder.settings.set_default("admin.port", admin_port)
    contextBuilder.settings.set_default("admin.webhook_urls", "")
    contextBuilder.settings.set_default("transport.inbound_configs", [["http", "0.0.0.0", inbound_port]])
    contextBuilder.settings.set_default("transport.outbound_configs", ["http"])

    contextBuilder.settings.set_default("default_label", "Aries Cloud Agency")
    contextBuilder.settings.set_default("default_endpoint", agency_endpoint + ":" + inbound_port)
    contextBuilder.settings.set_default("ledger.genesis_transactions", False)
    contextBuilder.settings.set_default("ledger.genesis_url", genesis_url)

    contextBuilder.settings.set_default("wallet.type", "Indy")

    # Debug params
    contextBuilder.settings.set_default("debug.auto_store_credential", True)
    contextBuilder.settings.set_default("debug.auto_accept_invites", True)
    contextBuilder.settings.set_default("debug.auto_accept_requests", True)
    contextBuilder.settings.set_default("debug.auto_respond_messages", True)
    contextBuilder.settings.set_default("debug.auto_respond_credential_proposal", True)
    contextBuilder.settings.set_default("debug.auto_respond_credential_offer", True)
    contextBuilder.settings.set_default("debug.auto_respond_credential_request", True)
    contextBuilder.settings.set_default("debug.auto_respond_presentation_proposal", True)
    contextBuilder.settings.set_default("debug.auto_respond_presentation_request", True)
    contextBuilder.settings.set_default("debug.auto_store_credential", True)

    # Create and Setup Conductor
    conductor = Conductor(contextBuilder)
    await conductor.setup()

    # Start
    await conductor.start()


def init():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    init()
