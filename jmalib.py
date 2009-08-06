# -*- coding: utf-8 -*-

import datetime

class RadarNowCast:
  @classmethod
  def create_radar_image_url(cls, area, time):
    url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar"
    url += "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "-00.png"
    return url

  @classmethod
  def create_nowcast_image_url(cls, area, time, no):
    url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast"
    url += "/" + ("%03i" % area)
    url += "/" + time.strftime("%Y%m%d%H%M")
    url += "-" + ("%02i" % no)
    url += ".png"
    return url

  @classmethod
  def create_image_url(cls, area, time, no):
    if no == 0:
      return cls.create_radar_image_url(area, time)
    else:
      return cls.create_nowcast_image_url(area, time, no)
