FROM python:3.8-buster as base
# Perform common operations, dependency installation etc... 
RUN pip install poetry
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter

FROM base as development
# Configure for local development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as production
# Configure for production
ENV FLASK_ENV=production
RUN poetry config virtualenvs.create false --local && poetry install && poetry add gunicorn
# PORT env variable is set by Heroku
ENTRYPOINT 'poetry run gunicorn "app:create_app()" --bind 0.0.0.0:$PORT'

FROM base as test
# Configure for testing
RUN poetry install
# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb \
    && apt-get update \
    && apt-get -f install ./chrome.deb -y \
    && rm ./chrome.deb
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && echo "Installing chromium webdriver version ${LATEST}" \
    && curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip \
    && apt-get install unzip -y \
    && unzip ./chromedriver_linux64.zip
ENV PYTHONPATH=.
ENTRYPOINT ["poetry", "run", "pytest", "-s"]
