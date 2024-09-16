FROM python:3.10

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY ./requirements/requirements.txt .
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=config.settings

COPY . .