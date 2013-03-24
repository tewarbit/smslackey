import unittest

from google.appengine.api import urlfetch
from google.appengine.ext import testbed
from app.handlers.smsrequesthandler import SmsRequestHandler
from mocks import pasteboard

from mocks import mocks

class SmsRequestHandlerTests(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

    mocks.init()


  def tearDown(self):
    self.testbed.deactivate()

    mocks.shutdown()


  def test_zipcode(self):
    expected = "zipcode set to 48103"
    self.do_test("set zip 48103", "7342394484", expected, True, "7342394484")

    expected = "48103"
    self.do_test("get zip", "7342394484", expected, True, "7342394484")

    expected = "zipcode set to 46901"
    self.do_test("set zip kokomo in", "7342394484", expected, True, "7342394484")

    expected = "46901"
    self.do_test("get zip", "7342394484", expected, True, "7342394484")    


  def test_weather(self):
    expected = ( "30F(~22). M: Overcast w snow showers, then mostly cloudy "
                 "w snow showers. H 34F, wchill 5F. E: Part cloudy w snow showers. "
                 "L 19F, wchill 10F." )
    
    self.do_test("w", "7342394484", expected, True, "7342394484")


  def test_movies(self):
    expected = ( "Jack .. Goodrich 1120 1350 1850 Rave 1045 1325 16 1835 2115 MJR 1430 1710 1950 2230" )

    self.do_test("jack", "7342394484", expected, True, "7342394484")


  def test_places(self):
    expected = ( "Address: 375 N Maple Rd, Ann Arbor, MI 48103  Phone:(734) 827-5000 Tuesday hours 8:00 am10:00 pm" )

    self.do_test("plum market", "7342394484", expected, True, "7342394484")


  def test_wikisearch(self):
    expected = ( "Defenestration is the act of throwing someone or something out of a window" )

    self.do_test("defenestrate", "7342394484", expected, True, "7342394484")


  def test_wolframalphasearch_simple(self):
    expected = ( "73 years 9 days" )

    self.do_test("how old is chuck norris", "7342394484", expected, True, "7342394484")


  def test_wolframalphasearch_pi(self):
    expected = ( "The constant pi, denoted pi, is a real number defined as the ratio of a circle's "
                 "circumference C to its diameter d = 2r, pi congr. C/d = C/(2r) It is also so..." )

    self.do_test("define pi", "7342394484", expected, True, "7342394484")


  def test_wolframalphasearch_circle(self):
    pass

  
  def do_test(self, query, from_num, expected, is_sms, to_num):
    pasteboard.clear()
    
    req = mocks.MockHttpRequest(query, from_num)
    handler = SmsRequestHandler()
    handler.request = req
    handler.post()

    result = pasteboard.twilio_messages['message']

    self.assertEqual(expected, result)
    self.assertEqual(is_sms, pasteboard.twilio_messages['is_sms'])
    self.assertEqual(to_num, pasteboard.twilio_messages['send_to'])    

    pasteboard.clear()    

