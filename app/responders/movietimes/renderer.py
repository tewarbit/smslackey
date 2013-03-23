"""
A bunch of methods for taking a map of movie titles to movie times and rendering it as
as single string that's less than CHAR_LIMIT characters (max character length for SMS). The main
entry point is render(movie_time_map)
"""

import re

CHAR_LIMIT = 160

def render(pairs):
  movie_title = pairs[0][0]

  response = render_movie_title(movie_title)
  for pair in pairs:
    response = response + " " + render_theater_name(pair[0]) + " " + render_movie_times(pair[1])

  if (len(response) > CHAR_LIMIT):
    return response[0:157] + "..."

  return response

def render_theater_name(name):
  theater_name_words = words(name)
  if ("the" == theater_name_words[0].lower()):
    return theater_name_words[1]

  return theater_name_words[0]


def words(phrase): return re.findall(r"[\w']+", phrase)  