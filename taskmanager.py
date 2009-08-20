# -*- coding: utf-8 -*-

import datetime
import logging
#from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue


#class Task(db.Model):
#  path = db.StringProperty(required=True)
#  time = db.DateTimeProperty(required=True)


class TaskTracker:
  def __init__(self, path):
    self.path      = path
    self.key       = "task_" + path
    self.completed = False

  def is_completed(self):
    if not self.completed:
      #records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
      #self.completed = (records.count() == 0)
      self.completed = not (memcache.get(self.key) == 1)
    return self.completed

  def push(self):
    logging.info("push task " + self.path)
    memcache.add(self.key, 1, 30)
    taskqueue.add(url = self.path, method="GET", params = {})

  def pop(self):
    logging.info("pop task " + self.path)
    memcache.delete(self.key)
    #records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
    #db.delete(records)


def add_task(path):
  #task = Task(path = path, time = datetime.datetime.now())
  #task.put()
  tracker = TaskTracker(path)
  tracker.push()
  #taskqueue.add(url = path, method="GET", params = {})
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
