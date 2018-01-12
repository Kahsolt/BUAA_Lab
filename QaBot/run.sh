#!/bin/bash

PY3='python3'
PY2='python2'

screen -dmS QA-Snake $PY2 QA-Snake/QA/server.py
screen -dmS QaBot $PY3 QaBot/bot.py

screen -list

if [ "$1" = "-s" ]; then
  exit 0
else
  screen -r QaBot
fi
