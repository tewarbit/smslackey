A "dumb phone" app. 

Written in Python. Runs on Google App Engine. Uses twilio.

To run locally: 
- Update 'config.py' with your twilio account information.
- Run start.sh
- go to http://localhost:8080


scripts:
  - start.sh : runs a dev app server locally with smslackey loaded
  - deploy.sh : deploys to Google App Engine
  - runtests.sh : runs the unit tests