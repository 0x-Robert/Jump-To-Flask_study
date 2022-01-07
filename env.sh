#!/bin/bash

cd ~/projects/myproject
export FLASK_APP=pybo
export FLASK_ENV=development
export APP_CONFIG_FILE=/home/ubuntu/projects/myproject/config/production.py
source /home/ubuntu/venvs/myproject/bin/activate
