#!/usr/bin/env bash
set -euo pipefail

az container create --resource-group trustnet-covid-initiative --name cloud-agency-container \
    --image "${REGISTRY_LOGIN_SERVER}/aries-cloud-agency-image:latest" \
    --registry-login-server "${REGISTRY_LOGIN_SERVER}" \
    --registry-username ${REGISTRY_USERNAME} \
    --registry-password ${REGISTRY_PASSWORD} \
    --dns-name-label agency \
    --location 'eastasia' \
    --cpu 1 \
    --memory 1 \
    --ports 2000 7000