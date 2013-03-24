#!/bin/bash

echo
echo "------"
echo "deploying app to Google App Engine"
echo "------"
echo

appcfg.py update .

echo
echo "------"
echo "app successfully deployed!"
echo "------"
echo