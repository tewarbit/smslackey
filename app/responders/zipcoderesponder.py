import logging
import re
import xml.etree.ElementTree as ET

from app.responders.wolframalpharesponder import WolframAlphaResponder
from app.db import lackeydb
from app.types.messages import SimpleSmsResponse

class ZipCodeResponder:
  
  def respond(self, request):
    contents = request.query.lower()
    
    if (contents.startswith('set zip')):
      return self.setzip(contents, request.from_num)
    elif (contents.startswith('get zip')):
      return self.getzip(request)

    return None


  def setzip(self, contents, from_num):
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
      
      lackeydb.set_zipcode(from_num, zipcode)
      return SimpleSmsResponse('zipcode set to ' + zipcode)


    return SimpleSmsResponse('zipcode not set, no zipcode found')


  def getzip(self, request):
    return SimpleSmsResponse(request.zip_code)