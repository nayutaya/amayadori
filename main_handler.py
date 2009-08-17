# -*- coding: utf-8 -*-

import os
import logging
import re
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import areamanager
import amayadori
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

    path = os.path.join(os.path.dirname(__file__), "views/top.html")
    html = template.render(path, values)
    self.response.out.write(html)

import time
class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    lnglat = (float(lng), float(lat))
    area = areamanager.AreaManager.get_nearest_area(lnglat)
    if area == None:
      self.error_message("範囲外です。")
      return

    xy = area.lnglat_to_xy(lnglat)

    radar_time = amayadori.get_radar_time()
    image_bin  = amayadori.get_image(area.code, radar_time, 0)
    image      = png.Png8bitPalette.load(image_bin)

    # MEMO: タスクの実験用コード
    #tracker0 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 0)
    #logging.info("task0 is_completed: " + str(tracker0.is_completed()))
    #tracker1 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 1)
    #tracker2 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 2)
    #tracker3 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 3)
    #tracker4 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 4)
    #tracker5 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 5)
    #tracker6 = taskmanager.TaskManager.add_cache_fetch_task(area.code, observed_time, 6)
    #logging.info("task0 is_completed: " + str(tracker0.is_completed()))
    #time.sleep(0.5)
    #logging.info("task0 is_completed: " + str(tracker0.is_completed()))
    #time.sleep(0.5)
    #logging.info("task0 is_completed: " + str(tracker0.is_completed()))

    rimage = radar.RadarImage(image)

    #xy = (370,85)
    rainfall = rimage.get_ballpark_rainfall(xy)

    # http://amayadori-opt.appspot.com/ のためのGoogle Maps API Key
    mapkey = "ABQIAAAA-ys93Qu6HH7Py3ElrvrGIxQGMNRpk4DlDb3SBK780CawkJsqbhR6Q77-5by3FYPdmP6wscv2utyMUQ"

    values = {
      "area": str(area.code),
      "lat": str(lnglat[1]),
      "lng": str(lnglat[0]),
      "x": str(xy[0]),
      "y": str(xy[1]),
      "current_value": str(rainfall),
      "mapkey": mapkey,
      "radar_time": radar_time.strftime("%Y%m%d%H%M"),
    }

    path = os.path.join(os.path.dirname(__file__), "views/view.html")
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


class TestPage(webapp.RequestHandler):
  def get(self):
    pass

if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/", TopPage),
      (r"/view/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)", ViewPage),
      (r"/docomo/iarea", DocomoIAreaRedirector),
      (r"/docomo/gps",   DocomoGpsRedirector),
      (r"/test",         TestPage),
    ],
    debug = True)
  run_wsgi_app(application)
