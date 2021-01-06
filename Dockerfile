ARG GO_VER=1.15.6
FROM golang:${GO_VER}-alpine

RUN apk --update add py-pip gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install in-toto
