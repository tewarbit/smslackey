import unittest

from google.appengine.ext import testbed
from app.responders.setzipcoderesponder import SetZipCodeResponder

class SetZipCodeResponderTests(unittest.TestCase):

  def setUp(self):
    app = 'smslackey'
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
    self.testbed.deactivate()


  def test_respond(self):
    
    class MockRequest:
      pass

    req = MockRequest()
    req.query = "set zip 48103"
    req.from_num = "7345556666"

    response = SetZipCodeResponder().respond(req)
    self.assertEqual("zipcode set to 48103", response.message)

