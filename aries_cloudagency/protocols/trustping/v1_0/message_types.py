"""Message type identifiers for Trust Pings."""

SPEC_URI = (
    "https://github.com/hyperledger/aries-rfcs/tree/"
    "527849ec3aa2a8fd47a7bb6c57f918ff8bcb5e8c/features/0048-trust-ping"
)
PROTOCOL_URI = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/trust_ping/1.0"

PING = f"{PROTOCOL_URI}/ping"
PING_RESPONSE = f"{PROTOCOL_URI}/ping_response"

NEW_PROTOCOL_URI = "https://didcomm.org/trust_ping/1.0"

NEW_PING = f"{NEW_PROTOCOL_URI}/ping"
NEW_PING_RESPONSE = f"{NEW_PROTOCOL_URI}/ping_response"

PROTOCOL_PACKAGE = "aries_cloudagency.protocols.trustping.v1_0"

MESSAGE_TYPES = {
    PING: f"{PROTOCOL_PACKAGE}.messages.ping.Ping",
    PING_RESPONSE: f"{PROTOCOL_PACKAGE}.messages.ping_response.PingResponse",
    NEW_PING: f"{PROTOCOL_PACKAGE}.messages.ping.Ping",
    NEW_PING_RESPONSE: f"{PROTOCOL_PACKAGE}.messages.ping_response.PingResponse",
}
