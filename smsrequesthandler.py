import webapp2
import logging
import collections
import re
import StringIO
import lxml.html
from google.appengine.api import urlfetch
from movietimes.movietimesresponder import MovieTimesResponder
from restaurants.restaurantsresponder import RestaurantsResponder
from caller.callerresponder import CallerResponder
from twilio.rest import TwilioRestClient
from config import twilio

class SmsRequestHandler(webapp2.RequestHandler):

  def sms_responders(self):
    return [MovieTimesResponder(), RestaurantsResponder(), CallerResponder()]

  def handle_post_request(self, request):
    response = None
    for responder in self.sms_responders():
      response = responder.respond(request)
      if (response is not None): return response

    return response

  def post(self):
    logging.info('Handling a post request')

    class SmsRequest:
      pass

    request = SmsRequest()
    request.query = self.request.get('Body')
    request.query_words = re.findall(r"[\w']+", request.query.lower())

    response = self.handle_post_request(request)
    logging.info('Got a response ' + response.message + ' from a responder')

    # logging.info(movie_times)
    self.response.out.write('<html><body>')
    self.response.out.write('got message from: ' + self.request.get('From') + '<br/>')
    self.response.out.write(' with contents: ' + self.request.get('Body') + '<br/>')
    self.response.out.write(' RespondSms is: ' + self.request.get('RespondSms') + '<br/>')

    # response = MovieTimeRenderer.render(movie_times)

    if ("True" == self.request.get('isWebRequest')):
      logging.info("Request came in via the webpage")
      if ("SMSResponse" == self.request.get('RespondSms')):
        client = TwilioRestClient(twilio['account'], twilio['token'])
        client.sms.messages.create(to="+17342394484", from_="+15012468526", body=response.message)
    else:
      logging.info("Recieved request from phone")
      client = TwilioRestClient(twilio['account'], twilio['token'])
      if not response.is_sms:
        client.calls.create(to=response.respond_to_num,
                            from_="+15012468526",
                            url="http://smslackey.appspot.com/saymessage")
      else:
        client.sms.messages.create(to="+17342394484", from_="+15012468526", body=response.message)

    self.response.out.write(response.message)

    self.response.out.write('</pre></body></html>')

  def get(self):
    self.response.out.write('got a "get" request')

