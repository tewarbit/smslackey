import webapp2
import logging
import collections
import re
import StringIO
import lxml.html
from google.appengine.api import urlfetch

class SmsRequestHandler(webapp2.RequestHandler):
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
			logging.info("Finding times for movie name: " + movie_name)
			movie_times = map(lambda uni: uni.encode('ascii', 'ignore'), movie.xpath('.//div[@class="times"]/span/text()'))
			movies.append((movie_name, movie_times))
		
		return movies
		
	def filter_out_movies(self, movie_infos, query):
		def filter_fn(val): return any((query.lower() in re.findall(r"[\w']+", item[0].lower())) for item in val)
		
		def filter_movies(movie_list):
			return [item for item in movie_list if query.lower() in re.findall(r"[\w']+", item[0].lower())]
		
		return collections.OrderedDict((k, filter_movies(v)) for k, v in movie_infos.iteritems() if filter_fn(v))
	
	def post(self):
		logging.info('Handling a post request')
		movie_times = self.get_movie_times()
		movie_times = self.filter_out_movies(movie_times, self.request.get('Body'))
		logging.info(movie_times)
		self.response.out.write('<html><body>')
		self.response.out.write('got message from: ' + self.request.get('From') + '<br/>')
		self.response.out.write(' with contents: ' + self.request.get('Body') + '<br/>')
		
		for k in movie_times.keys()[0:3]:
			self.response.out.write('<b>' + k + '</b>' + ' ' + str(movie_times[k]) + ' <br/>')
		self.response.out.write('</pre></body></html>')

	def get(self):
		self.response.out.write('got a "get" request')
	