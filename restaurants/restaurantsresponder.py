import webapp2
import logging
import lxml.html
import StringIO
from google.appengine.api import urlfetch

class RestaurantsResponder:
  def respond(request):
    url = "http://www.google.com/movies?hl=en&near=48103&dq=showtimes+48103&q=showtimes&sa=X"
    result = urlfetch.fetch(url)

    logging.info("Fetched URL. Parsing...")
    htmltree = lxml.html.parse(StringIO.StringIO(result.content))
    theaters = htmltree.xpath('//div[@class="theater"]')
    