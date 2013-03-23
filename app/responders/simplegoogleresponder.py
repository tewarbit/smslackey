import logging
import lxml.html
import StringIO
import urllib
from google.appengine.api import urlfetch

from app.types.messages import SimpleSmsResponse

class SimpleGoogleResponder:
  def respond(self, request):
    q = { 'q': request.query }
    encoded_q = urllib.urlencode(q)

    #need to set a browser User-Agent so google returns the necessary info
    result = urlfetch.fetch(url="http://www.google.com/search?client=safari&rls=en&" + encoded_q + "&ie=UTF-8&oe=UTF-8",
                            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'})

    htmltree = lxml.html.parse(StringIO.StringIO(result.content))
    info_block = htmltree.xpath('//div[@class="vk_ans vk_dgy answer_predicate"]')
    if (len(info_block) > 0):
      response = self.gettext(info_block[0])
      logging.info("Found simple google response: " + response)
      return SimpleSmsResponse(response)

    return None

  
  def gettext(self, elem):
    text = elem.text or ""
    for e in elem:
      text += self.gettext(e)
      if e.tail:
        text += e.tail
    return text