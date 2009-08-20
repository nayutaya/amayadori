# -*- coding: utf-8 -*-

import logging
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import amayadori
import timeutil
import areamanager
import png
import giflib
import jmalib


class IndexPage(webapp.RequestHandler):
  def get(self, area):
    area         = int(area)
    radar_time   = amayadori.get_radar_time()
    nowcast_time = amayadori.get_nowcast_time()

    links = []
    for areainfo in areamanager.areas:
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

    pngbin = amayadori.get_image(area, time, ordinal)

    self.response.headers["Content-Type"] = "image/png"
    self.response.out.write(pngbin)


class PartialReducedImage(webapp.RequestHandler):
  def get(self, area, time, ordinal, x, y):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)
    x, y    = int(x), int(y)

    sx = max([0, x - 20])
    sy = max([0, y - 20])
    dx = 41
    dy = 41

    pngbin = amayadori.get_image(area, time, ordinal)
    pngimg = png.Png8bitPalette.load(pngbin)

    gifimg = giflib.Image(dx, dy, 8)
    gifimg.allocate_color((192, 192, 192))

    # 色を単純化
    for yy in xrange(dy):
      for xx in xrange(dx):
        rgb1  = pngimg.get_color((sx + xx, sy + yy))
        rgb2  = jmalib.color_reduction(rgb1)
        index = gifimg.allocate_color(rgb2)
        gifimg.set_pixel((xx, yy), index)

    # ボーダーライン
    #border = gifimg.allocate_color((255, 255, 255))
    #for xx in xrange(dx):
    #  gifimg.set_pixel((xx, 0     ), border)
    #  gifimg.set_pixel((xx, dy - 1), border)
    #for yy in xrange(dy):
    #  gifimg.set_pixel((0     , yy), border)
    #  gifimg.set_pixel((dx - 1, yy), border)

    # センターマーク
    center = gifimg.allocate_color((32, 32, 32))
    for i in xrange(10):
      gifimg.set_pixel((i + 1,      dy / 2), center)
      gifimg.set_pixel((dx - i - 2, dy / 2), center)
      gifimg.set_pixel((dx / 2, i + 1     ), center)
      gifimg.set_pixel((dx / 2, dy - i - 2), center)

    self.response.headers["Content-Type"] = "image/gif"
    gifimg.write(self.response.out)


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/(\d{3})\.html",                               IndexPage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.png",               WholeImage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.(\d+)\.(\d+)\.gif", PartialReducedImage),
    ],
    debug = True)
  run_wsgi_app(application)
