FROM python:3.8
RUN mkdir  /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
# install dependencies
RUN pip install --upgrade pip
RUN apt-get install libpq-dev
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["sh", "./run.sh"]
