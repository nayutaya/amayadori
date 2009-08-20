# -*- coding: utf-8 -*-

import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import amayadori
import taskmanager
import timeutil


# for cron
class CacheClearTask(webapp.RequestHandler):
  def get(self):
    pass


# for task-queue
class RainfallTask(webapp.RequestHandler):
  def get(self, area, time, ordinal, x, y):
    area    = int(area)
    time    = timeutil.yyyymmddhhnn_to_datetime(time)
    ordinal = int(ordinal)
    cxy     = (int(x), int(y))

    amayadori.get_rainfall(area, time, ordinal, cxy)

    taskmanager.TaskTracker(path = self.request.path).clear()


if __name__ == "__main__":
  application = webapp.WSGIApplication(
    [
      (r"/task/cache/clear", CacheClearTask),
      (r"/task/rainfall/(\d{3})/(\d{12})/(\d{2})/(\d+)/(\d+)", RainfallTask),
    ],
    debug = True)
  run_wsgi_app(application)
