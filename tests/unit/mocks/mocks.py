from google.appengine.api import urlfetch
from app.handlers.smsrequesthandler import SmsRequestHandler

import pasteboard
import urlcache

class MockResponse:
  pass


def mockfetch(url, headers=None):
  # print "fetching url: " + url

  resp = MockResponse()
  cnt = urlcache.get(url)

  resp.content = cnt
  return resp


def mock_sendTwilioResponse(n, resp, send_to):
    pasteboard.twilio_messages['send_to'] = send_to
    pasteboard.twilio_messages['is_sms'] = resp.is_sms
    if not resp.is_sms:
      pasteboard.twilio_messages['respond_url'] = resp.respond_url
      pasteboard.twilio_messages['respond_to_num'] = resp.respond_to_num
    else:
      pasteboard.twilio_messages['message'] = resp.message


class MockHttpRequest:

  def __init__(self, body, from_num):
    self.body = body
    self.from_num = from_num

  def get(self, param):
    if param == "Body":
      return self.body
    elif param == "From":
      return self.from_num

    return None


originalfetch = urlfetch.fetch
originalsendtwilio = SmsRequestHandler.sendTwilioResponse

def init():
  urlfetch.fetch = mockfetch
  SmsRequestHandler.sendTwilioResponse = mock_sendTwilioResponse
  urlcache.init()

def shutdown():
  urlfetch.fetch = originalfetch
  SmsRequestHandler.sendTwilioResponse = originalsendtwilio