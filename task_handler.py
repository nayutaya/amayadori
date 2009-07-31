# -*- coding: utf-8 -*-

import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


# for cron
class CacheClearTask(webapp.RequestHandler):
  def post(self):
    logging.info("CacheClearTask")

# for task-queue
class CacheFetchTask(webapp.RequestHandler):
  def post(self, area, time, ordinal):
    logging.info("CacheFetchTask")


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/task/cache/clear",                          CacheClearTask),
      (r"/task/cache/fetch/(\d{3})/(\d{12})/(\d{2})", CacheFetchTask),
    ],
    debug = True)
  run_wsgi_app(application)
