#!/bin/bash
BASEDIR=$(dirname ${BASH_SOURCE:-$0})
if [ ! -f ~/.virtualenv/telematik-py/bin/activate ] 
  then
    ${BASEDIR}/create-env.sh
fi
echo Activating virtualenv
source ~/.virtualenv/telematik-py/bin/activate
pip install -r ${BASEDIR}/requirements.txt
