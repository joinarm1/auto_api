#!/bin/sh

export root=$(cd "$(dirname "$0")"; pwd)
virtualenv ${root}/venv
source ${root}/venv/bin/activate && pip install -r requirements.txt
