ARG VERSION=latest
FROM ubuntu:${VERSION}
LABEL DESCRIPTION="tg-bot-apod"
ENV PATH_ROOT=/home/app
VOLUME ["/www"]
WORKDIR ${PATH_ROOT}
COPY . ${PATH_ROOT}
RUN apt-get -y update && \
        apt-get -y upgrade && \
        apt-get install -y python3.9 && \
        apt-get install -y python3-pip && \
        pip install -r requirements
ENTRYPOINT ["python3", "bot.py"]