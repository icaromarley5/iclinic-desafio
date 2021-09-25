# pull official base image
FROM python:3.10.0rc1

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt