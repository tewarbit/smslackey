import logging
import urllib
from google.appengine.api import urlfetch

from app.config.config import wolfram_alpha


API_BASE_URL = "http://api.wolframalpha.com/v2/query"

def query(query):
  params = { 'appid': wolfram_alpha['appid'], 'input': query, 'format': 'plaintext' }
  encoded = urllib.urlencode(params)

  result = urlfetch.fetch(url=API_BASE_URL + "?" + encoded)
  return result.content

