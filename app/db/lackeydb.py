import logging

from google.appengine.ext import db

from app.types.models import ZipCode

def get_zipcode(num):
  q = db.GqlQuery("SELECT * "
                  "FROM ZipCode "
                  "WHERE phone_number = '" + num + "' ")

  return q.get()


def set_zipcode(num, zipcode):
  # the phone number servces as the DB id, only one zipcode entry per phone number
  zc = ZipCode(key_name=num)
  
  zc.phone_number = num
  zc.zipcode = zipcode
  zc.put()