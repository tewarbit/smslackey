import logging
import lxml.html

from movie import Movie

class Theater:
  
  def __init__(self, node):
    self.name = node.xpath('.//h2[@class="name"]/a')[0].text_content()

    movies = []
    movie_nodes = node.xpath('.//div[@class="movie"]')
    for movie in movie_nodes:
      movies.append(Movie(movie))

    self.movies = movies


  def get_movie(self, query):
    filtered = filter(lambda mov: mov.matches(query), self.movies)
    
    if (len(filtered) == 0): return None
    if (len(filtered) == 1): return filtered[0]

    return self.filter_imax_and_3d(query, filtered)


  def filter_imax_and_3d(self, query, filtered):
    """ 
    You may get imax/3d movies included in a query for a standard movie. This filters those out
    if you have multiple matches from the first filter
    """
    
    query = query.lower()

    query_imax = "imax" in query
    query_3d = "3d" in query

    if not query_imax and not query_3d:
      f = filter(lambda mov: not mov.is_imax and not mov.is_3d, filtered)
      if (len(f) > 0): return f[0]
      else: return filtered[0]

    if not query_imax and query_3d:
      f = filter(lambda mov: not mov.is_imax and mov.is_3d, filtered)
      if (len(f) > 0): return f[0]
      else: return filtered[0]

    if query_imax and not query_3d:
      f = filter(lambda mov: mov.is_imax and not mov.is_3d, filtered)
      if (len(f) > 0): return f[0]
      else: return filtered[0]

    return filtered[0]

