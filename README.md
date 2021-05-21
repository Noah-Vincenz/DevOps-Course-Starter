# Todo-App

## CI Builds

To view the application CI builds in Travis-CI visit: [https://travis-ci.com/github/Noah-Vincenz/DevOps-Course-Starter/builds](https://travis-ci.com/github/Noah-Vincenz/DevOps-Course-Starter/builds).

## Initial One-time Setup

To setup the application run
```bash
$ cp -n .env.template .env
```
to create a `.env` plain text file in the root directory of the project. 
This `.env` file is used by flask to set environment variables, enabling things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. Populate the following variables inside the `.env` file with the `todoDB` MongoDB database and `todos` collection details/credentials at `cluster0.huksc.mongodb.net`:
```
TODO_LIST_ID=... # your 'todo' list id
DOING_LIST_ID=... # your 'done' list id
DONE_LIST_ID=... # your 'done' list id
BOARD_ID=... # your board id
MONGO_USERNAME=... # your DB username
MONGO_PW=... # your DB password
```
Note that *.env* has been added to the gitignore file so that these secrets will not be commited to git.
Now, our app is ready to be tested (see _Running the tests_) and/or run (see _Running the app_).

## Running the tests

Following this, in order to be able to run the tests, first run:
```bash
$ poetry install
$ export PYTHONPATH=.
```
to install all dependencies from ```pyproject.toml``` and set the python path in the project environment. 
And then run (```-s``` flag to allow printing as part of tests):
```bash
$ poetry run pytest -s tests/unit
```
to run the project's unit tests and
```bash
$ poetry run pytest -s tests/integration
```
to run the project's integration tests only.

\
Alternatively, you can run the tests in a Docker container by running:
```bash
$ docker build --target test --tag todo-app:tests .
```
to build a test-mode docker image from ```Dockerfile```, followed by
```bash
$ docker run --env TODO_LIST_ID=<TODO_LIST_ID> --env DOING_LIST_ID=<DOING_LIST_ID> --env DONE_LIST_ID=<DONE_LIST_ID> --env BOARD_ID=<BOARD_ID> --env MONGO_USERNAME=<MONGO_USERNAME> --env MONGO_PW=<MONGO_PW> --env SECRET_KEY=<SECRET_KEY> todo-app:tests tests
```
to run all the tests (including end-to-end tests) in ```tests/``` by running the image. (Note: input the values for the environment variables)

## Running the app

There are multiple ways to start the app.

### Inside Docker Container
Firstly, the app can be started in development-mode inside a docker container by running:
```bash
$ docker-compose up -d
```

\
Secondly, you can run the app in production-mode by running:
```bash
$ docker build --target production --tag todo-app:prod .
```
to build a production-mode docker image from ```Dockerfile```, followed by
```bash
$ docker run --env-file .env -p 5000:5000 --mount type=bind,source="$(pwd)",target=/DevOps-Course-Starter todo-app:prod
```
to run the image in production-mode (Note: the above command is limited to unix shells).

### Inside Virtual Machine
Lastly, you can also run the app inside a VM by running:
```bash
$ vagrant up
```
This will set up the environment in the VM and start up the application. 

\
In any of the above cases, you should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app running.
