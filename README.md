hamu-bot
========

sample script for slackbot

## preinstall
```
git clone https://github.com/sharl/geeklets.git
cp geeklets/.amedas ~
cp geeklets/{amedas,amesh} ~/bin
```

- amesh use imagemagick

## prereq
```
pip install -r requirements.txt
```

## usage

```
$ SLACK_TOKEN=xoxb-hogehoge ./hamu-bot.py
```

## Appendix
```
make
SLACK_TOKEN=xoxb-hogehoge docker-compose up -d
```

## DB module

- initialize
```
./initdb.py init
```
to create table.

### name_history

- config.json
```
{
    "name_history": {
	"keyword": "email address"
    }
}
```

### switchbot.meter

- config.json
```
    "switchbot.meter": {
        "keyword": "wake word",
        "token": "<developer token>",
        "device": "<device ID>"
    }
```
