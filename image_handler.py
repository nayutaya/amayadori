# -*- coding: utf-8 -*-

import logging
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import amayadori
import timeutil
import areamanager
import cachemanager

AreaManager = areamanager.AreaManager

class IndexPage(webapp.RequestHandler):
  def get(self, area):
    area  = int(area)
    rtime = amayadori.get_radar_time()
    ntime = amayadori.get_nowcast_time()

    links = []
    for areainfo in AreaManager.areas:
      if areainfo.code == area:
        links.append("<b>" + areainfo.name + "</b>")
      else:
        links.append("<a href=\"/image/" + str(areainfo.code) + ".html\">" + areainfo.name + "</a>")

    values = {
      "area" : ("%03i" % area),
      "rtime": rtime.strftime("%Y%m%d%H%M"),
      "ntime": ntime.strftime("%Y%m%d%H%M"),
      "link" : "[ " + " | ".join(links) + " ]",
    }

    path = os.path.join(os.path.dirname(__file__), "views/image.html")
    html = template.render(path, values)
    self.response.out.write(html)


class WholeImage(webapp.RequestHandler):
  def get(self, area, time, ordinal):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)

    image = amayadori.get_image(area, time, ordinal)

    self.response.headers["Content-Type"] = "image/png"
    self.response.out.write(image)


class PartialImage(webapp.RequestHandler):
  def get(self, area, time, ordinal, x, y):
    import giflib
    image = giflib.Image(31, 31, 8)
    image.append_color((64, 64, 64))
    image.append_color((255, 0, 0))
    for i in range(31):
      image.set_pixel((i, i), 1)
      image.set_pixel((31 - i, i), 1)
    self.response.headers["Content-Type"] = "image/gif"
    image.write(self.response.out)


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/(\d{3})\.html",                               IndexPage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.png",               WholeImage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.(\d+)\.(\d+)\.gif", PartialImage),
    ],
    debug = True)
  run_wsgi_app(application)
