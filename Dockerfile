FROM bcgovimages/von-image:py36-1.14-1

USER root

ARG AGENCY_ADMIN_PORT
ARG AGENCY_ADMIN_API_KEY
ARG AGENCY_INBOUND_PORT
ARG AGENCY_ENDPOINT
ARG GENESIS_URL

RUN pip install aries-cloudagent
RUN pip install pickledb

WORKDIR /src
ADD . .

ENV admin_api_key=$AGENCY_ADMIN_API_KEY \
    admin_port=$AGENCY_ADMIN_PORT \
    agency_endpoint=$AGENCY_ENDPOINT \
    inbound_port=$AGENCY_INBOUND_PORT \
    genesis_url=$GENESIS_URL

RUN chmod +x init-agency.sh

CMD ["./init-agency.sh"]
