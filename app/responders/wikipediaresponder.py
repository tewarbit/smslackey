import logging
import lxml.html
import StringIO
import re

from app.clients import wikipediaclient
from app.responders import wikipediarenderer
from app.types.messages import SimpleSmsResponse

class WikipediaResponder:
  def respond(self, request):
    response = wikipediaclient.query(request.query)
    result = self.getresults(response)
    if not result:
      logging.info("No wikipedia page found for: " + request.query + " found a search results div")

    return result


  def getresults(self, html_response):
    htmltree = lxml.html.parse(StringIO.StringIO(html_response))
    searchresults = htmltree.xpath('//*[@id="mw-content-text"]/div[@class="searchresults"]')
    if (len(searchresults) > 0):
      return None
    else:
      first_para = htmltree.xpath('//*[@id="mw-content-text"]/p[1]')
      if (len(first_para) > 0):
        content = self.gettext_minus_sup_tags(first_para[0])
        content = wikipediarenderer.render(content)
        
        logging.info("Found content for wikipedia responder: " + content)
        return SimpleSmsResponse(content)
    
    return None


  
  def gettext_minus_sup_tags(self, elem):
    if elem.tag == 'sup': return ""

    text = elem.text or ""
    for e in elem:
      text += self.gettext_minus_sup_tags(e)
      if e.tail:
        text += e.tail
    
    return text    