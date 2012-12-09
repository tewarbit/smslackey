import webapp2
import logging
import lxml.html
import StringIO
import urllib
from lackeyresponse import LackeyResponse
from google.appengine.api import urlfetch

class RestaurantsResponder:
  def respond(self, request):
    q = { 'q': request.query + ' 48103' }
    encoded_q = urllib.urlencode(q)

    #need to set a browser User-Agent so google returns the necessary info
    result = urlfetch.fetch(url="http://www.google.com/search?client=safari&rls=en&" + encoded_q + "&ie=UTF-8&oe=UTF-8",
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'})

    htmltree = lxml.html.parse(StringIO.StringIO(result.content))
    info_block = htmltree.xpath('//div[@id="rhs_block"]')[0]
    addressNodes = info_block.xpath('//span[contains(.,"Address")]')
    if (len(addressNodes) == 0):
      logging.info("No business location found for request")
      return None

    address = addressNodes[0]
    response = self.gettext(address.getparent())
    response += ". "
    phone = info_block.xpath('//span[contains(.,"Phone")]')[0]
    response += self.gettext(phone.getparent())
    response += ". "
    hours = info_block.xpath('//div[@id="hour_now"]')[0]
    response += self.gettext(hours)
    return LackeyResponse(response.encode('ascii', 'ignore'), True, None)

  def is_ascii(self, s): return all(ord(c) < 128 for c in s)

  def gettext(self, elem):
    text = elem.text or ""
    for e in elem:
      text += self.gettext(e)
      if e.tail:
        text += e.tail
    return text      
    