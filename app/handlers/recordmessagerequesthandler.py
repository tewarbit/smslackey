import webapp2
import logging
import urllib

from xml.dom.minidom import Text

class RecordMessageRequestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("Recieved a request to record a message, responding with appropriate TwiML")

    msg_save_name = self.request.get('msg_name')
    from_num = self.request.get('from_number')
    
    params = { 'msg_name': msg_save_name, 'from_number': from_num }
    encoded = urllib.urlencode(params)
    
    #need to encode it as xml becase TwiML must be valid xml
    t = Text()
    t.data = encoded
    encoded = t.toxml()

    say_tag = """<Say voice="woman">record message after the tone.</Say>"""
    record_tag = """<Record action="http://smslackey.appspot.com/saverecording?%s"/>""" % encoded
    output = """<?xml version="1.0" encoding="UTF-8"?><Response>%(say)s%(rec)s</Response>""" % {"say": say_tag, "rec": record_tag}
    self.response.out.write(output)


  def post(self):
    self.get() 