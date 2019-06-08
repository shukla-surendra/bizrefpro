FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install -r /usr/src/app/requirements.txt
RUN apt update
#RUN apt install -y libmysqlclient
