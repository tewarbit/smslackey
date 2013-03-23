import logging
import re
import xml.etree.ElementTree as ET

from app.responders.wolframalpharesponder import WolframAlphaResponder
from app.types.models import ZipCode
from app.types.messages import SimpleSmsResponse

class SetZipCodeResponder:
  
  def respond(self, request):
    contents = request.query.lower()
    
    if (contents.startswith('set zip')):
      zipstring = contents[(len('set zip')):].strip()

      zipcode = None
      zips = re.findall(r"\d{5}", contents)
      if (len(zips) > 0): 
        zipcode = zips[0]
      else:
        response = WolframAlphaResponder().get_answer('zip code ' + zipstring)
        
        zips = re.findall(r"\d{5}", response)
        if (len(zips) > 0): 
          zipcode = zips[0]


      logging.info("The zipcode to be set is: " + zipcode)

      if (zipcode):
        if (type(zipcode) is unicode): zipcode = zipcode.encode('ascii', 'ignore')
        
        zc = ZipCode()
        zc.phone_number = request.from_num
        zc.zipcode = zipcode
        zc.put()
        return SimpleSmsResponse('zipcode set to ' + zipcode)


      return SimpleSmsResponse('zipcode not set, not zipcode found')

    return None
