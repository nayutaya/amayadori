# -*- coding: utf-8 -*-

import datetime

class RadarNowCast:
  @classmethod
  def create_observed_image_url(cls, area, time):
    url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar/"
    url += ("%03i" % area)
    url += "/"
    url += time.strftime("%Y%m%d%H%M")
    url += "-00.png"
    return url

  @classmethod
  def create_predictive_image_url(cls, area, time, no):
    url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/"
    url += ("%03i" % area)
    url += "/"
    url += time.strftime("%Y%m%d%H%M")
    url += "-"
    url += ("%02i" % no)
    url += ".png"
    return url
