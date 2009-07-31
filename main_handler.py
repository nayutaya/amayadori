# -*- coding: utf-8 -*-

import os
import logging
import re
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import area
import nowcast
import png
import radar
import taskmanager


class LatLng:
  @staticmethod
  def dms_to_deg(dms):
    regexp = re.compile(r"^([\+\-])?(\d+)\.(\d+)\.(\d+\.\d+)$")
    match  = regexp.match(dms)
    sign   = (1 if match.group(1) != "-" else -1)
    deg    = float(match.group(2))
    min    = float(match.group(3))
    sec    = float(match.group(4))
    return sign * (deg + (min / 60) + (sec / 3600))


class TopPage(webapp.RequestHandler):
  def get(self):
    values = {
      "redirect_url": "http://amayadori-opt.appspot.com/docomo/iarea",
    }

    path = os.path.join(os.path.dirname(__file__), "top.html")
    html = template.render(path, values)
    self.response.out.write(html)

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

    taskmanager.TaskManager.add_cache_fetch_task(nearest_area.code, observed_time, 0)

    rimage = radar.RadarImage(image)

    xy = (370,85)
    rainfall = rimage.get_ballpark_rainfall(xy)

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


class DocomoIAreaRedirector(webapp.RequestHandler):
  def post(self):
    lat  = self.request.get("LAT")
    lng  = self.request.get("LON")
    xacc = self.request.get("XACC")
    logging.info("docomo-iarea: lat=" + str(lat) + " lng=" + str(lng) + " xacc=" + str(xacc))

    lat_deg = "%.4f" % LatLng.dms_to_deg(lat)
    lng_deg = "%.4f" % LatLng.dms_to_deg(lng)
    self.redirect("/view/" + lat_deg + "/" + lng_deg)

  def get(self):
    self.response.out.write("")


class DocomoGpsRedirector(webapp.RequestHandler):
  def get(self):
    lat  = self.request.get("lat")
    lng  = self.request.get("lon")
    xacc = self.request.get("x-acc")
    logging.info("docomo-gps: lat=" + str(lat) + " lng=" + str(lng) + " xacc=" + str(xacc))

    lat_deg = "%.4f" % LatLng.dms_to_deg(lat)
    lng_deg = "%.4f" % LatLng.dms_to_deg(lng)
    self.redirect("/view/" + lat_deg + "/" + lng_deg)


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/", TopPage),
      (r"/view/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)", ViewPage),
      (r"/docomo/iarea", DocomoIAreaRedirector),
      (r"/docomo/gps",   DocomoGpsRedirector),
    ],
    debug = True)
  run_wsgi_app(application)
