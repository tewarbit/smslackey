
import re

class LackeyRequest:
  """ Contains details about the request """

  def __init__(self, query, from_num, zip_code):
    self.query = query
    self.from_num = from_num
    self.query_words = re.findall(r"[\w']+", query.lower())
    self.zip_code = zip_code


class SimpleSmsResponse:
  def __init__(self, msg):
    self.is_sms = True

    if (type(msg) is unicode): msg = msg.encode('ascii', 'ignore')
    self.message = msg


class InitiateCallResponse:
  def __init__(self, respond_num, url):
    self.is_sms = False
    self.message = "Calling number: " + respond_num + " with url: " + url
    self.respond_to_num = respond_num
    self.respond_url = url