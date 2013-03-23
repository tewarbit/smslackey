import webapp2
import logging
import app.config.config

from app.types.models import Recording

class SaveRecordingRequestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("Recieved request to save a recording")

    msg_name = self.request.get('msg_name')
    from_num = self.request.get('from_number')
    recording_url = self.request.get('RecordingUrl')

    logging.info("Saving recording named: %(msg)s, from %(num)s at %(rurl)s" % 
      {"msg": msg_name, "num": from_num, "rurl": recording_url})

    rec = Recording()
    rec.author = from_num
    rec.url = recording_url
    rec.name = msg_name

    rec.put()


  def post(self):
    self.get()
