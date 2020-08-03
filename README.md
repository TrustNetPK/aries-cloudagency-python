# Hyperledger Aries Cloud Agency - Python  <!-- omit in toc -->


<!-- ![logo](/docs/assets/aries-cloudagent-python-logo-bw.png) -->

> An easy to use multi-tenant aries agency enabling multiple individual users to set up their personal agent wallets and communicate with any Aries cloud agent python [(ACA-Py)](https://github.com/hyperledger/aries-cloudagent-python).

Hyperledger Aries Cloud Agency Python (ACAG-Py) is a foundation for building self-sovereign identity (SSI) / decentralized identity services running in non-mobile environments using DIDcomm messaging, the did:peer DID method, and verifiable credentials. With ACAG-Py, SSI developers can focus on building services using familiar web and mobile development technologies instead of trying to learn the nuts and bolts of low-level SDKs.


## Run locally

ACAG-Py can be run with docker without installation. It runs in combination with other agents to create a local workable enviornment.

See https://github.com/TrustNetPK/cov-id-cloud-agent for details.

## Usage

Command to create new wallet:

`http://AGENCY_URL/create_wallet`

```json
{
    "wallet_name": "walletname",
    "seed": "000000000000000000000000SomeSeed"
}
```

Headers to pass with every call except (create_wallet):

```
X-API-Key: secret
wallet-key: walletsecret
wallet-name: walletname
```

## Security

The administrative API exposed by the agent for the controller to use must be protected with an API key
(using the `--admin-api-key` command line arg) or deliberately left unsecured using the
`--admin-insecure-mode` command line arg. The latter should not be used other than in development if the API
is not otherwise secured.


> Storage and some other modules were modified in aca-py to create this multi-tenant agency. This particular code base requires security and storage improvements!


## API

Follows same api as ACA-PY with additional parameters in header see 'Usage' section.

## Credit

ACAG-PY is based on [ACA-Py](https://github.com/hyperledger/aries-cloudagent-python) and the initial implementation of ACA-Py was developed by the Verifiable Organizations Network (VON) team based at the Province of British Columbia. To learn more about VON and what's happening with decentralized identity in British Columbia, please go to [https://vonx.io](https://vonx.io).


## Disclaimer

ACAG-PY was developed in response the need dire of a multi-tenant-agency for mobile and web apps that can interact with aca-py. It's development is still in progress and is viable for PoC grade solutions and hasn't been tested in production. 

## License

[Apache License Version 2.0](https://github.com/hyperledger/aries-cloudagent-python/blob/master/LICENSE)
