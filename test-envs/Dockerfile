FROM ubuntu:latest
LABEL maintainer="157239q@gmail.com"
ENV DEBIAN_FRONTEND noninteractive
SHELL ["/bin/bash", "-c"]
RUN apt-get update &&\
	apt-get install -y vim curl wget git bzip2 htop build-essential &&\
	curl vim.kelvinho.org | bash
WORKDIR /base
#COPY Miniconda3-latest-Linux-x86_64.sh miniconda.sh
COPY Miniconda3-py37_4.8.2-Linux-x86_64.sh miniconda.sh
#COPY Miniconda3-4.5.4-Linux-x86_64.sh miniconda.sh
RUN bash ./miniconda.sh -b -p $HOME/miniconda && ~/miniconda/bin/conda init bash
COPY base /base
RUN cp /base/.bashrc ~/.bashrc

