# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


# for cron
class CacheClearTask(webapp.RequestHandler):
  def get(self):
    pass

class CacheFetchTask(webapp.RequestHandler):
  def get(self, area, date, ordinal):
    pass


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/task/cache/clear",                         CacheClearTask),
      (r"/task/cache/fetch/(\d{3})/(\d{8})/(\d{2})", CacheFetchTask),
    ],
    debug = True)
  run_wsgi_app(application)
