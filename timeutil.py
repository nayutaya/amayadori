# -*- coding: utf-8 -*-

import datetime
import re


def get_jst_now(utcnow = None):
  utcnow = utcnow or datetime.datetime.utcnow()
  return utcnow + datetime.timedelta(hours = 9)

def get_per_minute_time(time):
  return datetime.datetime(
    time.year, time.month, time.day,
    time.hour, time.minute)

def yyyymmddhhnn_to_datetime(str):
  regexp = re.compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$")
  match  = regexp.match(str)
  return datetime.datetime(
      int(match.group(1)), int(match.group(2)), int(match.group(3)),
      int(match.group(4)), int(match.group(5)))

def timedelta_to_second(delta):
  return (delta.days * 60 * 60 * 24) + delta.seconds

def timedelta_to_word(delta):
  second = timedelta_to_second(delta)
  if second <= 0:
    return str(-second / 60) + "分前"
  else:
    return str(second / 60) + "分後"
