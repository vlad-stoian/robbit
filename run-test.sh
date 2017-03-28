#!/usr/bin/env bash

postfacto_token=$(cat secrets.yml | yq -r '.["postfacto-token"]')
retro_id=$(cat secrets.yml | yq -r '.["retro-id"]')
slack_token=$(cat secrets.yml | yq -r '.["slack-token"]')
slack_channel="C4M632FNU"

echo "${postfacto_token}"
echo "${retro_id}"
echo "${slack_token}"
echo "${slack_channel}"

python3 ./src/post-retro-items.py "${postfacto_token}" "${retro_id}" "${slack_token}" "${slack_channel}"
python3 ./src/update-channel-topic.py "${slack_token}" "${slack_channel}"
