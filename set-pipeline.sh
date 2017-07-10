#!/usr/bin/env bash

if lpass status; then
  fly -t zumba sp -p rabbitmq-slacking-robbit -c robbit.yml --load-vars-from <(lpass show 'Shared-London Services/rabbitmq/robbit-secrets' --notes)
fi
