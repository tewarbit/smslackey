import lxml.html
import StringIO
import movietimerenderer

from theater import Theater


txt = open("times.html")
htmltree = lxml.html.parse(StringIO.StringIO(txt.read()))

matches = []

theaters = htmltree.xpath('//div[@class="theater"]')
for theater in theaters:
  t = Theater(theater)
  movie = t.get_movie("oz")
  if movie:
    # print t.name, movie.name
    matches.append((t, movie))

print movietimerenderer.render(matches[:3])