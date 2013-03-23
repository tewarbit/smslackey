import collections
import logging
import lxml.html
import movietimerenderer
import re
import StringIO
from google.appengine.api import urlfetch

from theater import Theater
from app.types.messages import SimpleSmsResponse

SHOWTIMES_URL = "http://www.google.com/movies?hl=en&near="


class MovieTimesResponder:
  
  def respond(self, request):
    url = SHOWTIMES_URL + request.zip_code + "&dq=showtimes+" + request.zip_code + "&q=showtimes&sa=X"
    result = urlfetch.fetch(SHOWTIMES_URL)
    htmltree = lxml.html.parse(StringIO.StringIO(result.content))

    matches = []

    theaters = htmltree.xpath('//div[@class="theater"]')
    for theater in theaters:
      t = Theater(theater)
      movie = t.get_movie(request.query)
      if movie:
        matches.append((t, movie))

    if (len(matches) == 0): return None

    response = movietimerenderer.render(matches[:3])
    logging.info("Responding from movie responder with: " + response)
    return SimpleSmsResponse(response)
    