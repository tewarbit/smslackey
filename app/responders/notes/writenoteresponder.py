import logging

from app.types.models import Note
from app.types.messages import SimpleSmsResponse

class WriteNoteResponder:
  def respond(self, request):
    if (request.query.lower().startswith('sm')):
      msg = request.query[2:].strip()

      logging.info("Saving msg: %(msg)s, from %(from_num)s" % {"msg": msg, "from_num": request.from_num})

      note = Note()
      note.author = request.from_num
      #note.author = "7342394484"
      note.content = msg
      note.put()

      return SimpleSmsResponse("Saved message")

    return None
