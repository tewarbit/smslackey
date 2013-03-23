import datetime

from google.appengine.ext import db

class Note(db.Model):
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class Recording(db.Model):
  author = db.StringProperty()
  name = db.StringProperty()
  url = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)


class ZipCode(db.Model):
  phone_number = db.StringProperty()
  zipcode = db.StringProperty()