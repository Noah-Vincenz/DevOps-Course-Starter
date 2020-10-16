# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. Add the following variables to the *.env* file:
```
API_KEY=... # your trello api key
API_TOKEN=... # your trello api token
TODO_LIST_ID=... # your 'todo' list id
DOING_LIST_ID=... # your 'done' list id
DONE_LIST_ID=... # your 'done' list id
TRELLO_BOARD_ID=... # your board id
```
Note that *.env* has been added to the gitignore file so that these secrets will not be commited to git.

Use poetry add to add any dependencies that you need e.g. 
```bash
$ poetry add requests
```

## Running the tests

Following this, you can then run all the test by running:
```bash
$ python -m pytest
```
or if you want to run the unit and integration tests only:
```bash
$ python -m pytest tests/unit_integration
```
or if you want to run the end-to-end tests only:
```bash
$ python -m pytest tests/e2e
```
## Running the app

Once the all dependencies have been installed and all tests succeed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
