ARG VERSION=latest
FROM ubuntu:${VERSION}
LABEL DESCRIPTION="tg-bot-apod"
ENV PATH_ROOT=/home/app
VOLUME ["/www"]
WORKDIR ${PATH_ROOT}
COPY . ${PATH_ROOT}
RUN apt-get -y update && \
        apt-get -y upgrade && \
        apt-get install -y python3-pip && \
        pip install ${PATH_ROOT}/nasaapi-1.0.0b0-py3-none-any.whl && \
        pip install -r requirements
ENTRYPOINT ["python3", "bot.py"]