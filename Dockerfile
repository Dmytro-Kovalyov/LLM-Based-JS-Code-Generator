FROM python:3.8.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN apt update
RUN apt -y install nodejs
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt