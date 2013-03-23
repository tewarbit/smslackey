import webapp2
import logging
import app.config.config

class SayMessageRequestHandler(webapp2.RequestHandler):
  def get(self):
    output = """<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="woman">"""
    output += config.message
    output += """</Say><Hangup/></Response>"""
    self.response.out.write(output)

  def post(self):
    self.get()
