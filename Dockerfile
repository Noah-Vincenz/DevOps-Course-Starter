FROM python:3.8-buster as base
# Perform common operations, dependency installation etc... 
RUN pip install poetry
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter
RUN poetry install

FROM base as development
# Configure for local development
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as production
# Configure for production
ENV FLASK_ENV=production
RUN poetry add gunicorn
ENTRYPOINT poetry run gunicorn "app:create_app()" --bind 0.0.0.0:5000

FROM base as test
# Configure for testing
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
ENV PORT=5000
ENTRYPOINT ["poetry", "run", "pytest", "-s"]
