#!/bin/bash

if [ "$FLASK_ENV" = "development" ]
then
    poetry run flask run --host=0.0.0.0
else
    poetry run gunicorn "app:create_app()" --bind 0.0.0.0:5000
fi