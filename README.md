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
docker build -t hamu-bot .
docker run -d -e SLACK_TOKEN=xoxb-hogehoge hamu-bot
```
