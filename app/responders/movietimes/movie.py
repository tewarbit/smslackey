import logging
import lxml.html
import re

class Movie:

  def __init__(self, node):
    self.name = node.xpath('.//div[@class="name"]/a')[0].text

    movie_text_content = node.text_content().encode('ascii', 'ignore')
    self.movie_times =  re.findall(r"\d{1,2}:\d\d[amp]{0,2}", movie_text_content)


  def matches(self, query):
    title_words = re.findall(r"[\w']+", self.name.lower())
    query_words = re.findall(r"[\w']+", query.lower())
    return all(map(lambda word: word in title_words, query_words))


  def is_imax(self): return "imax" in self.name.lower()


  def is_3d(self): return "3d" in self.name.lower()