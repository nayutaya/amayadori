# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class WholeImage(webapp.RequestHandler):
  def get(self):
    pass

class PartialImage(webapp.RequestHandler):
  def get(self):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/image/", WholeImage),
      (r"/image/", PartialImage),
    ],
    debug = True)
  run_wsgi_app(application)
