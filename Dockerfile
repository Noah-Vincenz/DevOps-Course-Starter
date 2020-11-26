FROM python:3.8-buster as base
# Perform common operations, dependency installation etc... 
RUN pip install poetry
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter/
RUN poetry install 

FROM base as development
# Configure for local development
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as production
# Configure for production
ENV FLASK_ENV=production
ENTRYPOINT poetry run gunicorn "app:create_app()" --bind 0.0.0.0:5000
