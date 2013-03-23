# -*- coding: utf-8 -*-

#!/usr/bin/python
import requests
import unittest

class TestPaperAPI(unittest.TestCase):

  def setUp(self):
    self.base_url = "http://smslackey.appspot.com/sms"

  def test_get_on_paper_returns_id_in_html(self):
    for id in 1,2,3:
      resp = requests.get(self.paper_url + str(id))
      self.assertEqual(resp.status_code, 200)
      self.assertEqual(resp.content, "<html><body>" + str(id) + "</body></html>")

  def test_get_on_nonexisting_paper_returns_404(self):
    self.assertEqual(resp.status_code, 404)

  def test_get_on_paper_returns_id_in_json(self):
    for id in 1,2,3:
      resp = requests.get(self.paper_url + str(id), headers=self.json_headers)
      self.assertEqual(resp.status_code, 200)
      self.assertEqual(resp.content, '{"id":' + '"' + str(id) + '",'\
                        '"title":'+ '"' + str(id) + '"}')