FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV POSTGRES_SERVER=localhost
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    libpq-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-setuptools \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS
RUN apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
RUN python3 -m nerd -d en_core_web_sm

RUN pip3 install -e .
RUN python3 -m graphvl -t

EXPOSE 8000

ENTRYPOINT ["graphvl-entrypoint.sh"]
