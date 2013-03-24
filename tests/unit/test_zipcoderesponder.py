import unittest

from google.appengine.ext import testbed
from app.responders.zipcoderesponder import ZipCodeResponder

from app.types.messages import LackeyRequest

class SetZipCodeResponderTests(unittest.TestCase):

  def setUp(self):
    app = 'smslackey'
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def tearDown(self):
    self.testbed.deactivate()


  def test_respond(self):
    
    req = LackeyRequest("set zip 90210", "7342223344", "48103")

    response = ZipCodeResponder().respond(req)
    self.assertEqual("zipcode set to 90210", response.message)

    req = LackeyRequest("get zip", "7342223344", "90210")
    response = ZipCodeResponder().respond(req)
    self.assertEqual("90210", response.message)


