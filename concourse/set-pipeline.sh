#!/usr/bin/env bash

if lpass status; then
  fly -t hh sp -p slacking-robbit -c robbit.yml \
    --load-vars-from <(lpass show 'Shared-PKS Telemetry/Robbit Pipeline Creds' --notes) \
    --var github-private-key="$(lpass show 'Shared-PKS Telemetry/[github] pkstelemetrybot-private-key' --notes)"
fi
