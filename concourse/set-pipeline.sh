#!/usr/bin/env bash

if lpass status; then
  fly -t rabbit sp -p slacking-robbit -c concourse/robbit.yml \
    --load-vars-from <(lpass show 'Shared-London Services/rabbitmq/robbit-secrets' --notes) \
    --var github-private-key="$(lpass show 'Shared-London Services/rabbitmq/robbit-github-key' --field="Private Key")"
fi
