# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class WholeImage(webapp.RequestHandler):
  def get(self, area, date, ordinal):
    pass

class PartialImage(webapp.RequestHandler):
  def get(self, area, date, ordinal, x, y):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/(\d{3})/(\d{8})/(\d{2})\.png",               WholeImage),
      (r"/image/(\d{3})/(\d{8})/(\d{2})\.(\d+)\.(\d+)\.gif", PartialImage),
    ],
    debug = True)
  run_wsgi_app(application)
