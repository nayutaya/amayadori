# -*- coding: utf-8 -*-

import datetime
import re


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

  @classmethod
  def is_water_color(cls, rgb):
    if   rgb == (192, 192, 192): return True
    elif rgb == (193, 193, 193): return True
    else:
      r, g, b = rgb
      return (b >= g)

  @classmethod
  def is_ground_color(cls, rgb):
    r, g, b = rgb
    return (g > b)

  @classmethod
  def color_reduction(cls, rgb):
    table = {
      (255,   0,   0): (255,   0,   0), # ‰J‰_    80mm/h ˆÈã
      (255,   0, 255): (255,   0, 255), # ‰J‰_ 50-80mm/h
      (255, 153,   0): (255, 153,   0), # ‰J‰_ 30-50mm/h
      (255, 255,   0): (255, 255,   0), # ‰J‰_ 20-30mm/h
      (  0, 255,   0): (  0, 255,   0), # ‰J‰_ 10-20mm/h
      (  0,   0, 255): (  0,   0, 255), # ‰J‰_  5-10mm/h
      ( 51, 102, 255): ( 51, 102, 255), # ‰J‰_  1- 5mm/h
      (153, 204, 255): (153, 204, 255), # ‰J‰_  0- 1mm/h
      ( 96,  57,  19): ( 96, 128,  96), # ŠÏ‘ª“_
      (230, 230, 230): (255, 255, 255), # “s“¹•{Œ§‹«ŠE
      (102, 102, 102): (102, 102, 102), # ŠCŠİ‹«ŠE/ƒOƒŠƒbƒh
      (255, 255, 255): (255, 255, 255), # ŠCŠİ‹«ŠE
      (116, 123, 114): (116, 123, 114), # ŠCŠİ‹«ŠE
      (160, 160, 160): (160, 160, 160), # ŠCŠİ‹«ŠE
    }
    ret = table.get(rgb)
    if ret == None:
      if cls.is_ground_color(rgb):
        return ( 96, 128,  96)
      elif cls.is_water_color(rgb):
        return ( 64,  96, 128)
      else:
        return (192,   0, 192)
    else:
      return ret
