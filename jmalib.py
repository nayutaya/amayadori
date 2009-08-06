# -*- coding: utf-8 -*-

import datetime
import re


class TimeUtility:
  @classmethod
  def get_jst_now(cls, utcnow = datetime.datetime.utcnow()):
    return utcnow + datetime.timedelta(hours = 9)

  @classmethod
  def get_per_minute_time(cls, time):
    return datetime.datetime(time.year, time.month, time.day, time.hour, time.minute)


class RadarNowCast:
  @classmethod
  def parse_radar_js(cls, src):
    regexp = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})-(\d{2})\.png")
    result = []

    for (year, month, day, hour, minute, ordinal) in regexp.findall(src):
      time = datetime.datetime(
        int(year), int(month), int(day),
        int(hour), int(minute))
      result.append((time, int(ordinal)))

    return result

  @classmethod
  def parse_nowcast_js(cls, src):
    regexp = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})-(\d{2})\.png")
    result = []

    for (year, month, day, hour, minute, ordinal) in regexp.findall(src):
      time = datetime.datetime(
        int(year), int(month), int(day),
        int(hour), int(minute))
      result.append((time, int(ordinal)))

    return result

  @classmethod
  def get_latest_time(cls, time_and_ordinals):
    times = [time for (time, ordinal) in time_and_ordinals]
    times.sort()
    return times[-1]

  @classmethod
  def get_current_radar_time(cls, fetcher):
    url    = "http://www.jma.go.jp/jp/radnowc/hisjs/radar.js"
    source = fetcher(url)
    parsed = cls.parse_radar_js(source)
    return cls.get_latest_time(parsed)

  @classmethod
  def get_current_nowcast_time(cls, fetcher):
    url    = "http://www.jma.go.jp/jp/radnowc/hisjs/nowcast.js"
    source = fetcher(url)
    parsed = cls.parse_nowcast_js(source)
    return cls.get_latest_time(parsed)

  @classmethod
  def create_radar_image_url(cls, area, time):
    url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar"
    url += "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "-00.png"
    return url

  @classmethod
  def create_nowcast_image_url(cls, area, time, ordinal):
    url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast"
    url += "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "-" + ("%02i" % ordinal)
    url += ".png"
    return url

  @classmethod
  def create_image_url(cls, area, time, ordinal):
    if ordinal == 0:
      return cls.create_radar_image_url(area, time)
    else:
      return cls.create_nowcast_image_url(area, time, ordinal)

  @classmethod
  def get_image(cls, area, time, ordinal, fetcher):
    url    = cls.create_image_url(area, time, ordinal)
    binary = fetcher(url)
    return binary
