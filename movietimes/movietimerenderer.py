import re

class MovieTimeRenderer:

  @staticmethod
  def render(movie_time_map):
    movie_title = movie_time_map[movie_time_map.keys()[0]][0][0]
    response = MovieTimeRenderer.render_movie_title(movie_title)
    for k in movie_time_map.keys()[0:3]:
      response = response + " " + MovieTimeRenderer.render_theater_name(k) + " " + MovieTimeRenderer.render_movie_times(movie_time_map[k][0][1])

    if (len(response) > 160):
      return response[0:157] + "..."
    return response

  @staticmethod
  def render_theater_name(name):
    theater_name_words = MovieTimeRenderer.words(name)
    if ("the" == theater_name_words[0].lower()):
      return theater_name_words[1]

    return theater_name_words[0]

  @staticmethod
  def words(phrase): return re.findall(r"[\w']+", phrase)

  @staticmethod
  def render_movie_time(movie_time): return MovieTimeRenderer.render_movie_title(movie_time[0]) + MovieTimeRenderer.render_movie_times(movie_time[1])

  @staticmethod
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

  @staticmethod
  def render_movie_times(movie_times): return " ".join([MovieTimeRenderer.to_24_format(x, MovieTimeRenderer.is_pm(i, movie_times)) for i, x in enumerate(movie_times)])

  @staticmethod
  def is_pm(index, movie_times):
    if movie_times[index].endswith('am'):
      return False
    elif movie_times[index].endswith('pm'):
      return True
    elif any(item.endswith('am') for item in movie_times[index:]):
      return False
    return True

  @staticmethod
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
      