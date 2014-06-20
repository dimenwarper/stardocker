# stardocker ("forked" from dockercluster by Louis Gioia [see https://bitbucket.org/lhgioia/dockercluster/])
#
# VERSION	0.0.1

FROM ubuntu:14.04
MAINTAINER Pablo Cordero <dimenwarper@gmail.com>

# make sure the package repository is up to date
RUN apt-get update -y

# install dependencies and vim editor
RUN apt-get install -y python-setuptools
RUN apt-get install -y autoconf
RUN apt-get install -y python-dev
RUN apt-get install -y vim
RUN apt-get install -y wget

# create StarCluster ssh key directory
RUN mkdir ~/.ssh

# install StarCluster
RUN easy_install StarCluster
RUN mkdir ~/.starcluster
RUN mkdir ~/.starcluster/plugins

# Copy local starcluster config file to container
COPY ~/.starcluster/config -O ~/.starcluster/config

# Copy stardocker plugin to container
RUN wget https://github.com/dimenwarper/stardocker/stardocker_config.py -O ~/.starcluster/plugins/stardocker_config.py
