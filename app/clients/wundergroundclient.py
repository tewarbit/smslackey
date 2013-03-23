import logging
import urllib
from google.appengine.api import urlfetch

from app.config.config import wunderground


API_BASE_URL = "http://api.wunderground.com/api/" + wunderground['key'] + "/conditions/hourly/forecast/q/"


def query(zipcode):
  api_url = API_BASE_URL + zipcode + ".json"
  result = urlfetch.fetch(url=api_url)
  return result.content

