import collections
import logging
import lxml.html
import movietimerenderer
import re
import StringIO
from lackeyresponse import LackeyResponse
from google.appengine.api import urlfetch

class MovieTimesResponder:
  def respond(self, request):
    movie_times = self.get_movie_times()
    movie_times = self.filter_out_movies(movie_times, request)
    if (len(movie_times) < 1): return None

    response = movietimerenderer.MovieTimeRenderer.render(movie_times)
    return LackeyResponse(response, True, None)

  def get_movie_times(self):
    logging.info('Looking up movie times')
    url = "http://www.google.com/movies?hl=en&near=48103&dq=showtimes+48103&q=showtimes&sa=X"
    result = urlfetch.fetch(url)

    logging.info("Fetched URL. Parsing...")
    htmltree = lxml.html.parse(StringIO.StringIO(result.content))
    theaters = htmltree.xpath('//div[@class="theater"]')
    logging.info('Found ' + str(len(theaters)) + ' theaters')

    movie_info = collections.OrderedDict()
    for theater in theaters:
      theater_name = theater.xpath('.//h2[@class="name"]/a')[0].text_content()
      movie_info[theater_name] = self.get_show_times(theater)

    return movie_info	

  def get_show_times(self, theater_node):
    movies = []

    movie_nodes = theater_node.xpath('.//div[@class="movie"]')
    logging.info('Found ' + str(len(movie_nodes)) + ' movies')
    for movie in movie_nodes:
      movie_name = movie.xpath('.//div[@class="name"]/a')[0].text
      unicode_movie_times = re.findall(r"\d{1,2}:\d\d[amp]{0,2}", movie.text_content())
      movie_times = map(lambda uni: uni.encode('ascii', 'ignore'), unicode_movie_times)
      movies.append((movie_name, movie_times))

    return movies

  def filter_out_movies(self, movie_infos, query):
    def filter_fn(val): return any(all(query_word in movie_title[0].lower() for query_word in query.query_words) for movie_title in val)

    return collections.OrderedDict((k, self.filter_movies(v, query)) for k, v in movie_infos.iteritems() if filter_fn(v))

  def filter_movies(self, movie_list, query):
    three_d_query = '3d' in query.query_words
    imax_query = 'imax' in query.query_words

    def movie_filter(movie_title):
      movie_words = re.findall(r"[\w']+", movie_title[0].lower())

      logging.info("Looking for query_words: " + str(query.query_words) + " in movie_words: " + str(movie_words))
      queried_movie = all(query_word in movie_words for query_word in query.query_words)
      if not queried_movie: return False

      three_d_movie = '3d' in movie_words
      imax_movie = 'imax' in movie_words
      logging.info("3d query: " + str(three_d_query) + " imax query: " + str(imax_query))
      logging.info("3d movie: " + str(three_d_movie) + " imax movie: " + str(imax_movie))
      return three_d_query == three_d_movie and imax_query == imax_movie

    filtered_movies = filter(movie_filter, movie_list)
    return filtered_movies
    