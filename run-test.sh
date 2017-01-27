#!/usr/bin/env bash

postfacto_token=$(cat secrets.yml | yq -r '.["postfacto-token"]')
retro_id=$(cat secrets.yml | yq -r '.["retro-id"]')
slack_token=$(cat secrets.yml | yq -r '.["slack-token"]')
slack_channel="test-robbit"

echo "${postfacto_token}"
echo "${retro_id}"
echo "${slack_token}"
echo "${slack_channel}"

python3 ./src/check-it.py "${postfacto_token}" "${retro_id}" "${slack_token}" "${slack_channel}"
