import webapp2
import logging


class WarmUpHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("Warming up the smslackey!")


  def post(self):
    self.get()
