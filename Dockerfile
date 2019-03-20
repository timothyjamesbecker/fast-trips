#fasttrips Ubuntu 16LTS image
FROM ubuntu:bionic
RUN apt-get update
RUN apt-get upgrade -y

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -y \
apt-utils \
build-essential \
g++ \
gfortran \
git \
wget \
nano \
libffi6 \
libffi-dev \
libssl1.0.0 \
libssl-dev \
libblas3 \
libblas-dev \
liblapack3 \
liblapack-dev \
libcurl4-openssl-dev \
libxml2-dev \
libncurses5-dev \
libbz2-dev \
zlib1g-dev \
python3 \
python3-dev \
python3-pip \
python3-numpy \
python3-scipy \
python3-sklearn \
python3-h5py
RUN apt-get autoremove
RUN pip3 install git+https://github.com/timothyjamesbecker/fast-trips.git@develop
ENV PYTHONPATH /usr/local/lib/python3.6/dist-packages/fasttrips
