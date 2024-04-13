# pull official base image
FROM python:3.11.1-slim

# install dev dependencies
# follow docker.com best practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# (for ex. using apt-get update alone in a RUN statement causes caching issues)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libsndfile1 \
    python3-dev \
    vim \
    libcurl4-openssl-dev \
    libssl-dev

EXPOSE 8000

# create directory for api_user
RUN mkdir -p /home/api_user

# create the api_user user
RUN useradd api_user --create-home

ENV USER_HOME=/home/api_user
ENV APP_HOME=/home/api_user/api
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the api_user user
RUN chown -R api_user:api_user $USER_HOME

# change to the app user
USER api_user

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up python env with poetry
ENV PATH=$USER_HOME/.local/bin:$PATH

# match poetry version with the one you're using for your project
RUN pip install --no-cache-dir poetry==1.8.2

RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev --no-root --compile
ENV PATH=$APP_HOME/.venv/bin:$PATH

CMD $APP_HOME/bin/start-daphne
