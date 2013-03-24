#!/bin/bash

echo
echo "------"
echo "Deploying app to Google App Engine"
echo "------"
echo

appcfg.py update .

echo
echo "------"
echo "App successfully deployed!"
echo "------"
echo

echo
echo "------"
echo "Running deployment tests"
echo "------"
echo

python -m unittest discover tests/deployment '*_tests.py' -v

echo
echo "------"
echo "Finished"
echo "------"
echo