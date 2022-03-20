FROM node:16-alpine
WORKDIR /usr/src/app

RUN apk add --no-cache python3 python3-dev py3-pip
RUN pip install -U pykakasi alkana beautifulsoup4

