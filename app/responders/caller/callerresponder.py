import logging
import re
import app.config.config

from app.types.messages import InitiateCallResponse

class CallerResponder:
  def respond(self, request):
    if ('call' in request.query.lower()):
      number_to_call = re.findall(r"[2-9]{2}\d{8}", request.query)[0]
      index_of_num = request.query.find(number_to_call)
      words_to_say = request.query[(index_of_num + len(number_to_call) + 1):]
      config.message = words_to_say

      number_to_call = "+1" + number_to_call
      logging.info("Making a call to: " + number_to_call + " with words: " + words_to_say)
      return InitiateCallResponse(number_to_call, "http://smslackey.appspot.com/saymessage")

    return None
