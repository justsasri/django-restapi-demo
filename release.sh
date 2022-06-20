#!/usr/bin/env bash

python ./manage.py migrate
python ./manage.py init_user
python ./manage.py collectstatic --noinput
