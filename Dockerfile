FROM python:3.6.8
RUN mkdir  /server
WORKDIR /server
COPY . /server
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apt-get install libpq-dev
RUN pip install pipenv
RUN pipenv install --skip-lock --system --dev
EXPOSE 8000
