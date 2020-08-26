#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
flask run --access-logfile - --error-logfile - mypass:app
