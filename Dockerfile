FROM python:3.9

WORKDIR /usr/src
COPY . /usr/src
RUN pip install -r requirements.txt
