FROM python:3.7
RUN mkdir  /server
# Install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /server
# install dependencies
RUN pip install --upgrade pip
RUN apt-get install libpq-dev
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /server
ENTRYPOINT ["sh", "./run.sh"]
