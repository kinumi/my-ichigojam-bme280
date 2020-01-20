#!/bin/sh
export FLASK_APP=/home/ubuntu/my-ichigojam-bme280/app.py
export LANG=ja_JP.UTF-8
/home/kunimi_ikeda/.pyenv/shims/flask run --debugger --reload -p 80 -h 0.0.0.0
