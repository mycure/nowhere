FROM ubuntu:17.10

RUN apt-get update

RUN apt-get install -y python3 python3-pip
RUN apt-get install -y ghostscript

WORKDIR /nowhere

ADD requirements.txt /nowhere/requirements.txt
ADD nowhere.py /nowhere/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/nowhere/nowhere.py"]
