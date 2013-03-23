import unittest
import lxml.html
import StringIO

from app.responders import weatherrenderer

w_string = ("35F(~33). M: Mostly cloudy with snow showers, then "
            "snow showers and a chance of rain in the afternoon. "
            "High of 39F with a windchill as low as 21F. E: Mostly "
            "cloudy with snow showers in the evening, then overcast "
            "with snow showers. Low of 23F with a windchill as low as 16F.")

class WeatherRendererTests(unittest.TestCase):
  def test_render(self):
    rendered = weatherrenderer.render(w_string)
    expected = ("35F(~33). M: Most cloudy w s-showers, s-showers/rain in "
                "the afternoon. H 39F, wchill 21F. E: Most cloudy w "
                "s-showers, ocast w s-showers. L 23F, wchill 16F.")
    
    self.assertEqual(expected, rendered)

