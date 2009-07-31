# -*- coding: utf-8 -*-

import datetime
import logging
from google.appengine.api.labs import taskqueue


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
    taskqueue.add(url=path, params={})
