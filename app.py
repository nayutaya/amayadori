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

class AreaInfo:
  def __init__(self, code, xy1, xy2, lnglat1, lnglat2):
    self.code    = code
    self.xy1     = xy1
    self.xy2     = xy2
    self.lnglat1 = lnglat1
    self.lnglat2 = lnglat2

  def x1(self): return self.xy1[0]
  def y1(self): return self.xy1[1]
  def x2(self): return self.xy2[0]
  def y2(self): return self.xy2[1]
  def dx(self): return self.x2() - self.x1()
  def dy(self): return self.y2() - self.y1()

  def lng1(self): return self.lnglat1[0]
  def lat1(self): return self.lnglat1[1]
  def lng2(self): return self.lnglat2[0]
  def lat2(self): return self.lnglat2[1]
  def dlng(self): return self.lng2() - self.lng1()
  def dlat(self): return self.lat1() - self.lat2()

kinki = AreaInfo(
  code    = 211,
  xy1     = ( 54,  93),
  xy2     = (473, 396),
  lnglat1 = (133, 36),
  lnglat2 = (138, 33))

print kinki
#print kinki.x1()
#print kinki.y1()
#print kinki.x2()
#print kinki.y2()
#print kinki.dx()
#print kinki.dy()
print kinki.lnglat1
print kinki.lng1()
print kinki.lat1()
print kinki.lnglat2
print kinki.lng2()
print kinki.lat2()
print kinki.dlng()
print kinki.dlat()
