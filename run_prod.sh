#!/bin/bash

# poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
poetry run gunicorn 
# poetry run python app.py