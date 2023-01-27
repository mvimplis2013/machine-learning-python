FROM python:buster

RUN apt update

RUN apt install -y \
  build-essential \
  libpq-dev \
  libssl-dev \
  libffi-dev \
  openssl \
  zlib1g-dev

RUN apt install -y \
  emacs \
  git \
  urllib3==1.27.1

#RUN apt install -y \
#  python3-pip \
#  python3.7-dev \

#RUN apt install -y \
#  python3.7

RUN git clone https://github.com/mvimplis2013/machine-learning-python.git

WORKDIR machine-learning-python

RUN python setup.py install