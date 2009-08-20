# -*- coding: utf-8 -*-

import datetime
import logging
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue


class TaskTracker:
  def __init__(self, path):
    self.path      = path
    self.key       = "task_" + path
    self.completed = False

  def is_completed(self):
    if not self.completed:
      self.completed = not (memcache.get(self.key) == 1)
    return self.completed

  def push(self):
    logging.info("push task " + self.path)
    memcache.add(self.key, 1, 30)
    taskqueue.add(url = self.path, method="GET", params = {})

  def pop(self):
    logging.info("pop task " + self.path)
    memcache.delete(self.key)


def add_task(path):
  tracker = TaskTracker(path)
  tracker.push()
  return tracker

def create_rainfall_task_path(area, time, ordinal, xy):
  x, y = xy
  url  = "/task/rainfall"
  url += ("/%03i" % area)
  url += time.strftime("/%Y%m%d%H%M")
  url += ("/%02i" % ordinal)
  url += ("/%i" % x)
  url += ("/%i" % y)
  return url

def add_rainfall_task(area, time, ordinal, xy):
  return add_task(create_rainfall_task_path(area, time, ordinal, xy))
