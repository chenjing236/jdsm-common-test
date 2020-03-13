FROM python:2.7-slim

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get update --fix-missing && \
    apt-get install -y wget ca-certificates vim git

RUN apt-get -y install gcc
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /root
