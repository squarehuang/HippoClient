FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install rsync -y

RUN apt-get install python -y
RUN apt-get install python-setuptools -y
RUN apt-get install python-pip -y