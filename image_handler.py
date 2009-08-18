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
import png
import giflib
import jmalib

AreaManager = areamanager.AreaManager

class IndexPage(webapp.RequestHandler):
  def get(self, area):
    area         = int(area)
    radar_time   = amayadori.get_radar_time()
    nowcast_time = amayadori.get_nowcast_time()

    links = []
    for areainfo in AreaManager.areas:
      if areainfo.code == area:
        links.append("<b>" + areainfo.name + "</b>")
      else:
        links.append("<a href=\"/image/" + str(areainfo.code) + ".html\">" + areainfo.name + "</a>")

    values = {
      "area" : ("%03i" % area),
      "radar_time": radar_time.strftime("%Y%m%d%H%M"),
      "nowcast_time": nowcast_time.strftime("%Y%m%d%H%M"),
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


class WholeReducedImage(webapp.RequestHandler):
  def get(self, area, time, ordinal):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)

    image = amayadori.get_image(area, time, ordinal)

    pngimg = png.Png8bitPalette.load(image)
    gifimg = giflib.Image(150, pngimg.bitmap.height, 8)
    gifimg.allocate_color((192, 192, 192))

    width, height = (gifimg.width(), gifimg.height())
    for y in xrange(height):
      for x in xrange(width):
        rgb1  = pngimg.get_color((x + 200, y))
        rgb2  = jmalib.RadarNowCast.color_reduction(rgb1)
        index = gifimg.allocate_color(rgb2)
        gifimg.set_pixel((x, y), index)

    self.response.headers["Content-Type"] = "image/gif"
    gifimg.write(self.response.out)


class PartialReducedImage(webapp.RequestHandler):
  def get(self, area, time, ordinal, x, y):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)
    x, y    = int(x), int(y)

    image = amayadori.get_image(area, time, ordinal)

    sx = x - 15 if x >= 15 else 0
    sy = y - 15 if y >= 15 else 0
    dx = 31
    dy = 31

    pngimg = png.Png8bitPalette.load(image)

    image = giflib.Image(31, 31, 8)
    image.allocate_color((192, 192, 192))

    for yy in range(dy):
      for xx in range(dx):
        rgb   = pngimg.get_color((sx + xx, sy + yy))
        index = image.allocate_color(rgb)
        image.set_pixel((xx, yy), index)

    self.response.headers["Content-Type"] = "image/gif"
    image.write(self.response.out)


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/(\d{3})\.html",                               IndexPage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.png",               WholeImage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.gif",               WholeReducedImage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.(\d+)\.(\d+)\.gif", PartialReducedImage),
    ],
    debug = True)
  run_wsgi_app(application)
