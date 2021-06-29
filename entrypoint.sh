#!/bin/bash
export SLACK_TOKEN=${SLACK_TOKEN}
UID=${UID:-9999}
GID=${GID:-9999}
USER=hamu

groupadd -g ${GID} ${USER}
useradd  -g ${GID} -u ${UID} -m ${USER}
cp geeklets/.amedas ~${USER}

exec gosu ${USER} python3 ./hamu-bot.py
