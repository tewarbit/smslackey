import webapp2
import logging
import lxml.html
import StringIO
import urllib
from google.appengine.api import urlfetch

class TesterRequestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("Handling tester request")

    request = 'pizza house'
    q = { 'q': request + ' 48103' }
    encoded_q = urllib.urlencode(q)

    result = urlfetch.fetch(url="http://www.google.com/search?client=safari&rls=en&" + encoded_q + "&ie=UTF-8&oe=UTF-8",
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'})

    htmltree = lxml.html.parse(StringIO.StringIO(result.content))
    info_block = htmltree.xpath('//div[@id="rhs_block"]')[0]
    addressNodes = info_block.xpath('//span[contains(.,"Address")]')
    if (len(addressNodes) == 0):
      logging.info("No business location found for request")
    else:
      address = addressNodes[0]
      logging.info(self.gettext(address.getparent()))
      phone = info_block.xpath('//span[contains(.,"Phone")]')[0]
      logging.info(self.gettext(phone.getparent()))
      hours = info_block.xpath('//div[@id="hour_now"]')[0]
      logging.info(self.gettext(hours))


  def gettext(self, elem):
    text = elem.text or ""
    for e in elem:
      text += self.gettext(e)
      if e.tail:
        text += e.tail
    return text

