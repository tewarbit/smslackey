"""
Handles posts with contents of an SMS. Delegates the contents to a list of
responders, handing back the contents of the first valid response. See 
sms_responders() for list of currently registered responders
"""

import webapp2
import logging
import collections
import re
import string
import StringIO
import lxml.html
from google.appengine.api import urlfetch
from google.appengine.ext import db
from twilio.rest import TwilioRestClient

from app.config.config import twilio
from app.config.config import zipcode
from app.responders.movietimes.movietimesresponder import MovieTimesResponder
from app.responders.weatherresponder import WeatherResponder
from app.responders.placesresponder import PlacesResponder
from app.responders.caller.callerresponder import CallerResponder
from app.responders.setzipcoderesponder import SetZipCodeResponder
from app.responders.simplegoogleresponder import SimpleGoogleResponder
from app.responders.notes.writenoteresponder import WriteNoteResponder
from app.responders.recorder.recorderresponder import RecorderResponder
from app.responders.playmessageresponder import PlayMessageResponder
from app.responders.wolframalpharesponder import WolframAlphaResponder
from app.responders.wikipediaresponder import WikipediaResponder

from app.types.messages import LackeyRequest

class SmsRequestHandler(webapp2.RequestHandler):

  # Add in responders here to support additional queries. They are executed in order
  def sms_responders(self):
    return [ WriteNoteResponder(), 
             RecorderResponder(), 
             PlayMessageResponder(), 
             SetZipCodeResponder(), 
             MovieTimesResponder(), 
             WeatherResponder(), 
             PlacesResponder(), 
             CallerResponder(), 
             WikipediaResponder(), 
             WolframAlphaResponder()]


  def post(self):

    from_number = self.validateInputNumber(self.request.get('From'))
    zip_code = self.get_zip_code(from_number)
    logging.info("Looking up results relative to zipcode: %s" % zip_code)
    req = LackeyRequest(self.request.get('Body'), from_number, zip_code)
    
    logging.info('Handling a post request from: %(num)s with body: %(q)s' % {"num": from_number, "q": req.query})
    resp = self.get_response(req)

    self.handle_response(from_number, resp)


  def get_response(self, request):
    response = None
    for responder in self.sms_responders():
      response = responder.respond(request)
      if (response is not None): return response

    return response


  def handle_response(self, from_number, response):
    if not response:
      logging.info("No response found")
    else:
      logging.info('Got a response ' + response.message + ' from a responder')

      isTwilioResponse = False
      if not from_number:
        self.renderHtmlResponse(response)
      else:
        isTwilioResponse = True

      if isTwilioResponse:
        self.sendTwilioResponse(response, from_number)    


  def renderHtmlResponse(self, resp):
    self.response.out.write(resp.message) 
  
  
  def sendTwilioResponse(self, resp, send_to):
    # self.renderHtmlResponse(resp)
    # return None

    client = TwilioRestClient(twilio['account'], twilio['token'])
    if not resp.is_sms:
      client.calls.create(to=resp.respond_to_num,
                          from_=twilio['number'],
                          url=resp.respond_url)
    else:
      client.sms.messages.create(to=send_to, from_=twilio['number'], body=resp.message)


  def validateInputNumber(self, num):
    if not num: return None

    # num comes in as unicode, ain't nobody got time for that
    num = num.encode('ascii', 'ignore')

    num = num.translate(None, string.punctuation).translate(None, string.whitespace)
    if num.startswith("1"): num = num[1:]

    if (len(num) == 10): return num

    return None


  def get_zip_code(self, num):
    if not num: num = "X"

    q = db.GqlQuery("SELECT * "
                    "FROM ZipCode "
                    "WHERE phone_number = '" + num + "' ")

    z_code = q.get()
    if not z_code: return zipcode
    
    
    zipcodestring = z_code.zipcode
    if (type(zipcodestring) is unicode): zipcodestring = zipcodestring.encode('ascii', 'ignore')

    if (len(zipcodestring) != 5): return zipcode

    zipcodestring = zipcodestring.translate(None, string.punctuation).translate(None, string.whitespace)
    if (len(zipcodestring) != 5): return zipcode

    if (self.is_int(zipcodestring)): return zipcodestring

    return zipcode

  
  def is_int(self, s):
    try:
      int(s)
      return True
    except ValueError:
      return False


  def get(self):
    self.response.out.write('This is a response to a GET request. Send a POST to do something interesting')

