FROM python:3.6.8
RUN mkdir  /server
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /server
COPY Pipfile Pipfile.lock /server/
# install dependencies
RUN pip install --upgrade pip
RUN apt-get install libpq-dev
RUN pip install pipenv
RUN pipenv install --skip-lock --system --dev

COPY . /server
ENTRYPOINT ["sh", "./run.sh"]
CMD ["dev", "8000"]
