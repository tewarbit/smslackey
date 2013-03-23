import logging
import re
import urllib

from google.appengine.ext import db
from app.types.messages import InitiateCallResponse

BASE_URL = "http://smslackey.appspot.com/playrecording?"

class PlayMessageResponder:
  def respond(self, request):
    if (request.query.lower().startswith('pr')):
      number_to_call = re.findall(r"[2-9]{2}\d{8}", request.query)[0]

      msg_name = request.query[2:].replace(number_to_call, "").strip()

      logging.info("Looking for msg named: %(msg)s to play for: %(num)s" % {"msg": msg_name, "num": number_to_call})

      recordings = db.GqlQuery("SELECT * "
                               "FROM Recording "
                               "WHERE name = '" + msg_name + "' "
                               "ORDER BY date DESC")
      
      rec = recordings[0]

      params = { 'msg_url': rec.url }
      encoded = urllib.urlencode(params)
      url = BASE_URL + encoded
      logging.info("responder to record message request, going to URL: " + url)

      number_to_call = "+1" + number_to_call
      return InitiateCallResponse(number_to_call, url)


    return None
