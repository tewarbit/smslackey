#!/bin/bash

###
# Runs tests for smsLackey. Takes one argument - should be either 'deploy' or 'unit'
# If 'unit', runs local unit tests. Otherwise runs deployment tests against version
# deployed to http://smslackey.appspot.com. If no argument is given, defaults to 'unit'
###


if [ "$1" == deploy ]; then
  echo "------"
  echo "Running deploy tests"
  echo "------"
  python -m unittest discover tests/deployment '*_tests.py' -v
else
  echo "------"
  echo "Running unit tests"
  echo "------"
  python tests/test_runner.py /usr/local/google_appengine tests/unit
fi
