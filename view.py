# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import area
import nowcast
import png
import radar

class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    lnglat = (float(lng), float(lat))
    nearest_area = area.AreaManager.get_nearest_area(lnglat)
    if nearest_area == None:
      self.error_message("範囲外です。")
      return

    xy = nearest_area.lnglat_to_xy(lnglat)

    observed_time = nowcast.get_current_observed_time()
    image_bin     = nowcast.get_image(nearest_area.code, observed_time, 0)
    image         = png.Png8bitPalette.load(image_bin)

    rimage = radar.RadarImage(image)

    xy = (370,85)
    rainfall = rimage.get_rainfall(xy)

    values = {
      "area_code": str(nearest_area.code),
      "lat": str(lnglat[1]),
      "lng": str(lnglat[0]),
      "x": str(xy[0]),
      "y": str(xy[1]),
      "current_value": str(rainfall),
    }

    path = os.path.join(os.path.dirname(__file__), "view.html")
    html = template.render(path, values)

    self.response.out.write(html)

  def error_message(self, message):
    path = os.path.join(os.path.dirname(__file__), "error.html")
    html = template.render(path, {"message": message})
    self.response.out.write(html)


application = webapp.WSGIApplication(
  [(r"/view/([\+\-]?\d+(?:\.\d+)?)/([\+\-]?\d+(?:\.\d+)?)", ViewPage)],
  debug = True)


if __name__ == "__main__":
  run_wsgi_app(application)
