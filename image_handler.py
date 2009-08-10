# -*- coding: utf-8 -*-

import logging
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import nowcast
import timeutil


class IndexPage(webapp.RequestHandler):
  def get(self, area):
    area  = int(area)
    otime = nowcast.get_current_observed_time()
    ptime = nowcast.get_current_predictive_time()

    values = {
      "area":  ("%03i" % area),
      "otime": otime.strftime("%Y%m%d%H%M"),
      "ptime": ptime.strftime("%Y%m%d%H%M"),
    }

    path = os.path.join(os.path.dirname(__file__), "image.html")
    html = template.render(path, values)
    self.response.out.write(html)


class WholeImage(webapp.RequestHandler):
  def get(self, area, time, ordinal):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)

    image = nowcast.get_image(area, time, ordinal)

    self.response.headers["Content-Type"] = "image/png"
    self.response.out.write(image)


class PartialImage(webapp.RequestHandler):
  def get(self, area, time, ordinal, x, y):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/(\d{3})\.html",                               IndexPage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.png",               WholeImage),
      (r"/image/(\d{3})/(\d{12})/(\d{2})\.(\d+)\.(\d+)\.gif", PartialImage),
    ],
    debug = True)
  run_wsgi_app(application)
