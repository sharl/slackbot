from python:latest

ENV TZ Asia/Tokyo

RUN apt-get update && apt-get -y upgrade && apt-get install -y gosu git jq imagemagick
COPY hamu-bot.py .
COPY requirements.txt .
COPY modules modules/

# preinstall
RUN git clone https://github.com/sharl/geeklets.git
RUN cp geeklets/.amedas ~
RUN mkdir -p /usr/local/bin
RUN cp geeklets/amedas geeklets/amesh /usr/local/bin
# prereq
RUN pip3 install -r requirements.txt

COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
