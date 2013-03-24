# -*- coding: utf-8 -*-

#!/usr/bin/python
import requests
import unittest

class TestSMSLackeyAPI(unittest.TestCase):

  def setUp(self):
    self.base_url = "http://smslackey.appspot.com/sms"
    self.headers = {'Content-Length': '0', 'Accept-Encoding': 'gzip,deflate,sdch', 'Accept': '*/*'}

  def test_wolframalpha(self):
    payload = {'Body': 'define defenestrate'}
    resp = requests.post(self.base_url, params=payload, headers=self.headers)
    self.assertEqual("verb | throw through or out of the window", resp.content)

  def test_wikipedia(self):
    payload = {'Body': 'donkey cheese'}
    resp = requests.post(self.base_url, params=payload, headers=self.headers)
    self.assertEqual("Pule cheese, or just pule, is a cheese made from the milk of Balkan donkeys from Serbia.", 
                     resp.content)

