# -*- coding: utf-8 -*-

import datetime
import logging
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

import model


class TaskManager:
  @classmethod
  def create_cache_fetch_task_path(cls, area, time, ordinal):
    url  = "/task/cache/fetch"
    url += "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "/" + ("%02i" % ordinal)
    return url

  @classmethod
  def add_cache_fetch_task(cls, area, time, ordinal):
    path = cls.create_cache_fetch_task_path(area, time, ordinal)
    logging.info("task: " + path)

    task = model.Task(path = path, time = datetime.datetime.now())
    task.put()

    taskqueue.add(url=path, params={})

    return TaskTracker(path = path)

class TaskTracker:
  def __init__(self, path):
    self.path = path

  def is_completed(self):
    records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
    return (records.count() == 0)

  def clear(self):
    records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
    db.delete(records)
