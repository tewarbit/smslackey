import logging
import urllib
from google.appengine.api import urlfetch


API_BASE_URL = "http://www.google.com/search?client=safari&rls=en&"

def query(query, zipcode):
  q = { 'q': query + ' ' + zipcode }
  encoded_q = urllib.urlencode(q)

  #need to set a browser User-Agent so google returns the necessary info
  result = urlfetch.fetch(url=API_BASE_URL + encoded_q + "&ie=UTF-8&oe=UTF-8", 
                          headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'})

  return result.content
