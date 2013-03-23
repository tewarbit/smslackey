import logging
import json

from app.clients import wundergroundclient
from app.responders import weatherrenderer
from app.types.messages import SimpleSmsResponse

class WeatherResponder:
  def respond(self, request):
    logging.info("weather responder is looking at the query: " + request.query.lower())
    if (request.query.lower().strip() == "w" or request.query.lower().strip() == "weather"):
      wunder_response = wundergroundclient.query(request.zip_code)
      j_resp = json.loads(wunder_response)
      
      temp_f = j_resp["current_observation"]["temp_f"]
      temp_f = int(round(temp_f))
      response = "%dF" % temp_f

      feelslike_f = j_resp["current_observation"]["feelslike_f"]
      response += "(~%s). " % feelslike_f

      forcasts = j_resp["forecast"]["txt_forecast"]["forecastday"]
      morning_forcast_sentences = forcasts[0]["fcttext"].split('.')
      morning_forcast = morning_forcast_sentences[0].strip() + '. ' + morning_forcast_sentences[1].strip()

      #either the 2nd or 3rd sentence contains the hi or low for the day, we want this
      if (not self.hasHiLoTemp(morning_forcast_sentences[1])):
        morning_forcast += ' ' + morning_forcast_sentences[2].strip() + '. '
      else:
        morning_forcast += '. '

      response = response + 'M: ' + morning_forcast

      evening_forcast_sentences = forcasts[1]["fcttext"].split('.')
      evening_forcast = evening_forcast_sentences[0].strip() + '. ' + evening_forcast_sentences[1].strip()

      ##either the 2nd or 3rd sentence contains the hi or low for the day, we want this
      if (not self.hasHiLoTemp(evening_forcast_sentences[1])):
        evening_forcast += ' ' + evening_forcast_sentences[2].strip() + '. '
      else:
        evening_forcast += '. '

      response = response + 'E: ' + evening_forcast

      response = weatherrenderer.render(response.strip())
      logging.info("Response from weather responder: " + response)
      return SimpleSmsResponse(response)


  def hasHiLoTemp(self, forecast):
    return "High of" in forecast or "Low of" in forecast


