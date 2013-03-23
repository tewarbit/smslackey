import logging
import urllib
from google.appengine.api import urlfetch


API_BASE_URL = "http://en.wikipedia.org/w/index.php?"

def query(query):
  params = { 'search': query }
  encoded = urllib.urlencode(params)

  logging.info("fetching wiki url: " + API_BASE_URL + encoded)
  result = urlfetch.fetch(url=API_BASE_URL + encoded)
  return result.content

