import unittest
import lxml.html
import StringIO

from app.responders.wikipediaresponder import WikipediaResponder

class WikipediaResponderTests(unittest.TestCase):
  def test_getresults(self):
    txt = open("tests/unit/wikipedia.html")
    w = WikipediaResponder()
    r = w.getresults(txt.read())
    self.assertEqual("Defenestration is the act of throwing someone or something out of a window", r.message)

