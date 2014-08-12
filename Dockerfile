# Docker Magpie
# VERSION 0.1

FROM ubuntu:14.04

MAINTAINER Bill Thornton <billt2006@gmail.com>

# make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get update

# Install dependencies
RUN apt-get install -y build-essential python2.7 python2.7-dev python-pip git
ADD requirements.txt /usr/share/magpie/requirements.txt
RUN pip install -r /usr/share/magpie/requirements.txt
# Install magpie
ADD ./ /usr/share/magpie
RUN pip install -e /usr/share/magpie

EXPOSE 8080

ENTRYPOINT ["magpie"]
