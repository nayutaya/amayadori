# -*- coding: utf-8 -*-

import datetime
import logging
import StringIO
import struct
import binascii
import zlib

import nowcast
import png


print "Content-Type: text/plain"
print ""

#time  = nowcast.get_current_observed_time()
#image = nowcast.get_image(211, time, 0)

#png = png.Png8bitPalette.load(image)
#print png

import math

class AreaInfo:
  def __init__(self, code, gxy1, gxy2, glnglat1, glnglat2):
    self.code     = code
    self.gxy1     = gxy1
    self.gxy2     = gxy2
    self.glnglat1 = glnglat1
    self.glnglat2 = glnglat2

  def gx1(self): return self.gxy1[0]
  def gy1(self): return self.gxy1[1]
  def gx2(self): return self.gxy2[0]
  def gy2(self): return self.gxy2[1]
  def gdx(self): return self.gx2() - self.gx1()
  def gdy(self): return self.gy2() - self.gy1()

  def glng1(self): return self.glnglat1[0]
  def glat1(self): return self.glnglat1[1]
  def glng2(self): return self.glnglat2[0]
  def glat2(self): return self.glnglat2[1]
  def gdlng(self): return self.glng2() - self.glng1()
  def gdlat(self): return self.glat1() - self.glat2()

  def lng_to_x(self, lng):
    return int((lng - self.glng1()) / (float(+self.gdlng()) / self.gdx()) + self.gx1())

  def lat_to_y(self, lat):
    return int((lat - self.glat2()) / (float(-self.gdlat()) / self.gdy()) + self.gy2())

  def lnglat_to_xy(self, lnglat):
    return (self.lng_to_x(lnglat[0]), self.lat_to_y(lnglat[1]))

kinki = AreaInfo(
  code     = 211,
  gxy1     = ( 54,  93),
  gxy2     = (473, 396),
  glnglat1 = (133, 36),
  glnglat2 = (138, 33))

print kinki
print kinki.gxy1
#print kinki.gx1()
#print kinki.gy1()
print kinki.gxy2
#print kinki.gx2()
#print kinki.gy2()
print kinki.gdx()
print kinki.gdy()
print kinki.glnglat1
#print kinki.glng1()
#print kinki.glat1()
print kinki.glnglat2
#print kinki.glng2()
#print kinki.glat2()
print kinki.gdlng()
print kinki.gdlat()
print kinki.lng_to_x(135.18359)
print kinki.lat_to_y(34.67902)
print kinki.lnglat_to_xy((135.18359, 34.67902))
