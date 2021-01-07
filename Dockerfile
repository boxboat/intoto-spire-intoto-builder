ARG GO_VER=1.15.6
FROM golang:${GO_VER}-alpine

RUN apk --update add py-pip gcc musl-dev python3-dev libffi-dev openssl-dev docker git && \
    pip install in-toto

WORKDIR /app
COPY ./root.layout /root/root.layout
