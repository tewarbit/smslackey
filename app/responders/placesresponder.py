import logging
import lxml.html
import StringIO

from app.clients import googleplacesclient
from app.types.messages import SimpleSmsResponse

class PlacesResponder:
  def respond(self, request):
    response = googleplacesclient.query(request.query, request.zip_code)

    htmltree = lxml.html.parse(StringIO.StringIO(response))
    info_field = htmltree.xpath('//div[@id="rhs_block"]//fieldset')
    if (len(info_field) == 0):
      logging.info("No business location found for request")
      return None
    
    text = ""
    for e in info_field[0]:
      node_text = self.gettext(e)
      if (self.is_interesting(node_text)):
        text += node_text
      else:
        hours = e.xpath('.//div[@id="hour_now"]')
        if (len(hours) > 0):
          text += self.gettext(hours[0])


    strip_from = text.rfind('pm')
    if (strip_from != -1):
      text = text[:strip_from+2]


    logging.info("Info from places responder: " + text)
    logging.info("type of response is: " + str(type(text)))
    
    return SimpleSmsResponse(text.strip())


  def is_interesting(self, text):
    return "Address" in text or "Phone" in text


  def gettext(self, elem):
    text = elem.text or ""
    for e in elem:
      text += self.gettext(e)
      if e.tail:
        text += e.tail
    return text       