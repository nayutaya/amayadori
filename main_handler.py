# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class TopPage(webapp.RequestHandler):
  def get(self):
    pass

class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    pass

class DocomoIAreaRedirector(webapp.RequestHandler):
  def get(self):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/", TopPage),
      (r"/view/([\-]?\d+(?:\.\d+)?)/([\-]?\d+(?:\.\d+)?)", ViewPage),
      (r"/docomo/iarea", DocomoIAreaRedirector),
    ],
    debug = True)
  run_wsgi_app(application)
