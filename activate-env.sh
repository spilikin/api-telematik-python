#!/bin/bash
BASEDIR=$(dirname ${BASH_SOURCE:-$0})
if [ ! -f ~/.virtualenv/py-test-konauth/bin/activate ] 
  then
    ${BASEDIR}/create-env.sh
fi
echo Activating virtualenv
source ~/.virtualenv/py-test-konauth/bin/activate
pip install -r ${BASEDIR}/requirements.txt
