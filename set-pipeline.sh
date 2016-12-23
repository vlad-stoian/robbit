#!/usr/bin/env bash

if lpass status; then
  fly -t lite sp -p rabbot-retro -c rabbot.yml --load-vars-from <(lpass show 'Personal/robbit-secrets' --notes)
fi
