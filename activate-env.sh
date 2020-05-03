#!/bin/bash
BASEDIR=$(dirname ${BASH_SOURCE:-$0})
if [ ! -f ~/.virtualenv/api-telematik-python/bin/activate ] 
  then
    ${BASEDIR}/create-env.sh
fi
echo Activating virtualenv
source ~/.virtualenv/api-telematik-python/bin/activate
pip install -r ${BASEDIR}/requirements.txt
git submodule init
git submodule update
