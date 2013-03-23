import logging
import re
import urllib

from app.types.messages import InitiateCallResponse

BASE_URL = "http://smslackey.appspot.com/recordmessage?"

class RecorderResponder:
  def respond(self, request):
    if (request.query.lower().startswith('rm')):
      msg_save_name = request.query[2:].strip()
      logging.info("recording message with message name: " + msg_save_name)

      params = { 'msg_name': msg_save_name, 'from_number': request.from_num }
      encoded = urllib.urlencode(params)
      url = BASE_URL + encoded
      logging.info("responder to record message request, going to URL: " + url)

      return InitiateCallResponse(request.from_num, url)

    return None
