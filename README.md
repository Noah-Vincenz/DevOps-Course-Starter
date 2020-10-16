# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, add the following variables to the *.env* file:
```
API_KEY=... # your trello api key
API_TOKEN=... # your trello api token
TODO_LIST_ID=... # your 'todo' list id
DOING_LIST_ID=... # your 'done' list id
DONE_LIST_ID=... # your 'done' list id
TRELLO_BOARD_ID=... # your board id
```
Note that *.env* has been added to the gitignore file so that these secrets will not be commited to git.

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

If all tests succeed, start the Flask app by running:
```bash
$ flask run
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
