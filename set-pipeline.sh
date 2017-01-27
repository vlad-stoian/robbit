#!/usr/bin/env bash

if lpass status; then
  fly -t lite sp -p slacking-robbit -c robbit.yml --load-vars-from <(lpass show 'Personal/robbit-secrets' --notes)
fi
