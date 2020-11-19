FROM python:3.8-buster as base
# Perform common operations, dependency installation etc... 
RUN apt-get update && apt-get install -y \
    curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin" APP_PORT=5000
EXPOSE ${APP_PORT}
COPY . /app

FROM base as production
# Configure for production
COPY ./run_prod.sh ./run_prod.sh
RUN chmod +x ./run_prod.sh \ 
    && cd app \
    && poetry install
ENTRYPOINT ["./run_prod.sh"]

FROM base as development
# Configure for local development
COPY ./run_dev.sh ./run_dev.sh
RUN chmod +x ./run_dev.sh \
    && cd app \
    && poetry install
ENTRYPOINT ["./run_dev.sh"]
