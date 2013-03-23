"""
A bunch of methods for rendering a list of pairs (theather, movie) and rendering it as
as single string that's less than CHAR_LIMIT characters (max character length for SMS).
"""

import re

CHAR_LIMIT = 160

def render(pairs):
  movie_title = pairs[0][1].name

  response = render_movie_title(movie_title)
  for pair in pairs:
    response = response + " " + render_theater_name(pair[0].name) + " " + render_movie_times(pair[1].movie_times)

  if (len(response) > CHAR_LIMIT):
    return response[0:157] + "..."

  return response


def render_theater_name(name):
  theater_name_words = words(name)
  if ("the" == theater_name_words[0].lower()):
    return theater_name_words[1]

  return theater_name_words[0]


def words(phrase): return re.findall(r"[\w']+", phrase)


def render_movie_time(movie_time): 
  return render_movie_title(movie_time[0]) + render_movie_times(movie_time[1])


def render_movie_title(title):
  movie_3d = "3d" in title.lower()
  movie_imax = "imax" in title.lower()
  cropped = title

  if (len(title) > 7):
    cropped = title[0:5] + ".."
  if (movie_imax):
    cropped = cropped + " imax"
  if (movie_3d):
    cropped = cropped + " 3d"

  return cropped


def render_movie_times(movie_times): 
  return " ".join([to_24_format(x, is_pm(i, movie_times)) for i, x in enumerate(movie_times)])

def is_pm(index, movie_times):
  if movie_times[index].endswith('am'):
    return False
  elif movie_times[index].endswith('pm'):
    return True
  elif any(item.endswith('am') for item in movie_times[index:]):
    return False

  return True


def to_24_format(time_str, pm_time):
  parts = time_str.split(":")
  hours = parts[0]
  mins = parts[1]
  if (not pm_time and time_str.endswith('00')):
    return hours
  elif (not pm_time):
    return hours + mins[0:2]
  elif (pm_time and time_str.endswith('00')):
    return str(int(hours) + 12)
  else:
    return str(int(hours) + 12) + mins[0:2]


      