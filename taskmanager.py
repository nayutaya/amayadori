# -*- coding: utf-8 -*-

import datetime
import logging

class TaskManager:
  @staticmethod
  def create_cache_fetch_task_url(area, time, ordinal):
    print (area, time, ordinal)
    url  = "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "/" + ("%02i" % ordinal)
    return url

print TaskManager.create_cache_fetch_task_url(1,datetime.datetime.now(),3)
