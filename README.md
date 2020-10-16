# DevOps Apprenticeship: Project Exercise

## Setup

To setup the application run 
```bash
$ vagrant provision # needed to be run only once for initial setup
```
This will set up the application environment and download required dependencies. A file called `.env` will have been created with the environment variables below. This `.env` file is used by flask to set environment variables. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. Populate the following variables inside the `.env` file with your Trello App API details/credentials:
```
API_KEY=... # your trello api key
API_TOKEN=... # your trello api token
TODO_LIST_ID=... # your 'todo' list id
DOING_LIST_ID=... # your 'done' list id
DONE_LIST_ID=... # your 'done' list id
TRELLO_BOARD_ID=... # your board id
```
Note that *.env* has been added to the gitignore file so that these secrets will not be commited to git.

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

Once the all dependencies have been installed and all tests succeed, start the Flask app in development mode within the poetry environment inside a VM by running:
```bash
$ vagrant up
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app running in your VM.
