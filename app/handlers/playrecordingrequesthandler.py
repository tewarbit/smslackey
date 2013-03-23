import webapp2
import logging
import app.config.config

from app.types.models import Recording


class PlayRecordingRequestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("Recieved request to play a recording")

    msg_url = self.request.get('msg_url')
    output = """<?xml version="1.0" encoding="UTF-8"?><Response><Play>"""
    output += msg_url
    output += """</Play><Hangup/></Response>"""
    self.response.out.write(output)


  def post(self):
    self.get()
