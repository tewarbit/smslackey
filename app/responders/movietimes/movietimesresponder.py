import collections
import logging
import lxml.html
import movietimerenderer
import re
import StringIO
from google.appengine.api import urlfetch

from theater import Theater
from app.types.messages import SimpleSmsResponse

SHOWTIMES_URL_BASE = "http://www.google.com/movies?hl=en&near="


class MovieTimesResponder:
  
  def respond(self, request):
    movies_url = SHOWTIMES_URL_BASE + request.zip_code + "&dq=showtimes+" + request.zip_code + "&q=showtimes&sa=X"

    logging.debug("Fetching URL: %s" % movies_url)
    result = urlfetch.fetch(url=movies_url,
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'})

    
    htmltree = lxml.html.parse(StringIO.StringIO(result.content))

    matches = []

    theaters = htmltree.xpath('//div[@class="theater"]')
    for theater in theaters:
      t = Theater(theater)
      movie = t.get_movie(request.query)
      if movie:
        matches.append((t, movie))

    if (len(matches) == 0): 
      logging.info("No movies found containing query: %s" % request.query)
      return None

    response = movietimerenderer.render(matches[:3])
    logging.info("Responding from movie responder with: " + response)
    return SimpleSmsResponse(response)
    