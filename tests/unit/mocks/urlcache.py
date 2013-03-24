from app.config.config import wunderground
from app.config.config import wolfram_alpha

urlcache = {}

def init():
  url = "http://api.wunderground.com/api/" + wunderground['key'] + "conditions/hourly/forecast/q/48103.json"
  urlcache[url] = open("tests/unit/mocks/weather.json").read()

  url = "http://www.google.com/movies?hl=en&near=48103&dq=showtimes+48103&q=showtimes&sa=X"
  urlcache[url] = open("tests/unit/mocks/movie_times.html").read()

  url = "http://www.google.com/search?client=safari&rls=en&q=plum+market+48103&ie=UTF-8&oe=UTF-8"
  urlcache[url] = open("tests/unit/mocks/google_places.html").read()

  url = "http://en.wikipedia.org/w/index.php?search=defenestrate"
  urlcache[url] = open("tests/unit/wikipedia.html").read()

  url = "http://api.wolframalpha.com/v2/query?input=how+old+is+chuck+norris&format=plaintext&appid=" + wolfram_alpha['appid']
  urlcache[url] = open("tests/unit/mocks/simple_wolfram_alpha.xml").read()

  url = "http://api.wolframalpha.com/v2/query?input=define+pi&format=plaintext&appid=" + wolfram_alpha['appid']
  urlcache[url] = open("tests/unit/mocks/definepi_wolfram_alpha.xml").read()

  url = "http://api.wolframalpha.com/v2/query?input=zip+code+kokomo+in&format=plaintext&appid=" + wolfram_alpha['appid']
  urlcache[url] = open("tests/unit/mocks/zipcode_wolfram_alpha.xml").read()

def get(url):
  
  # first check if it has the exact URL in the cache
  if url in urlcache:
    return urlcache[url]
  
  # if not, see if it has some generic results for a url that starts with the same prefix of the requested url
  if (url.startswith("http://api.wunderground")):
    return open("tests/unit/mocks/weather.json").read()
  elif (url.startswith("http://www.google.com/movies")):
    return open("tests/unit/mocks/movie_times.html").read()
  elif (url.startswith("http://www.google.com/search?")):
    return open("tests/unit/mocks/generic_google_places.html").read()
  elif (url.startswith("http://en.wikipedia.org/w/index.php?")):
    return "<wikihtml></wikihtml>"
  elif (url.startswith("http://api.wolframalpha.com/v2/")) :
    return "<wolframalphaxml></wolframalphaxml>"