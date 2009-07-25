# -*- coding: utf-8 -*-

import datetime
import logging
import StringIO
import struct
import binascii
import zlib

import nowcast
import png
import area


logging.getLogger().setLevel(logging.DEBUG)


print "Content-Type: text/plain"
print ""


import math



def dump_matrix(matrix):
  for row in matrix:
    print "|" + " ".join(["%4.1f" % val for val in row]) + " |"

def interpolate_rain77(src77):
  dst77 = [[float(src77[y][x]) for x in range(7)] for y in range(7)]

  for y in range(1, 6):
    for x in range(1, 6):
      if src77[y][x] < 0:
        points = []
        points.append(src77[y - 1][x - 1])
        points.append(src77[y - 1][x    ])
        points.append(src77[y - 1][x + 1])
        points.append(src77[y    ][x - 1])
        points.append(src77[y    ][x + 1])
        points.append(src77[y + 1][x - 1])
        points.append(src77[y + 1][x    ])
        points.append(src77[y + 1][x + 1])
        available_points = [val for val in points if val >= 0]
        if len(available_points) > 0:
          avg = float(sum(available_points)) / len(available_points)
        else:
          avg = 0
        dst77[y][x] = avg

  return tuple([tuple(row) for row in dst77])

def window55(src77):
  return tuple([tuple([float(src77[y + 1][x + 1]) for x in range(5)]) for y in range(5)])

def weighted_average55(v55, w55):
  vwsum = 0.0
  wsum  = 0.0

  for y in range(5):
    for x in range(5):
       vwsum += v55[y][x] * w55[y][x]
       wsum  += w55[y][x]

  if wsum == 0.0: return 0.0
  return vwsum / wsum

m77 = (
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0),
  ( 0, 0, 0, 0, 0, 0, 0))

n = -1
m77 = (
  ( 1, 2, 3, 0, 0, 0, 0),
  ( 4, n, n, n, 0, 0, 0),
  ( 6, 7, 8, 0, 0, 9, 0),
  ( 0, n, 0, 0, 0, 8, 0),
  ( 0, 1, 0, n, 0, 7, 0),
  ( 0, 2, 3, 4, 5, 6, 0),
  ( 0, 0, 0, 0, 0, 0, 0))

#dump_matrix(m77)

#print "---"
#x77 = interpolate_rain77(m77)
#dump_matrix(x77)
#print x77

#print "---"
#x55 = window55(x77)
#dump_matrix(x55)

v55 = (
  (0.0, 0.0, 9.0, 0.0, 0.0),
  (0.0, 9.0, 9.0, 9.0, 0.0),
  (9.0, 9.0, 9.0, 9.0, 9.0),
  (0.0, 9.0, 9.0, 9.0, 0.0),
  (0.0, 0.0, 9.0, 0.0, 0.0))

w55 = (
  (0.6, 0.7, 0.8, 0.7, 0.6),
  (0.7, 0.8, 0.9, 0.8, 0.7),
  (0.8, 0.9, 1.0, 0.9, 0.8),
  (0.7, 0.8, 0.9, 0.8, 0.7),
  (0.6, 0.7, 0.8, 0.7, 0.6))

#dump_matrix(v55)
#print "---"
#dump_matrix(w55)
#print weighted_average55(v55, w55)

# PNGイメージの(x,y)を中心に7x7のパレットインデックスを取得
def pindex77(png, xy):
  sx, sy = xy
  return [[png.bitmap.bitmap[sy + y - 3][sx + x - 3] for x in range(7)] for y in range(7)]


def color77(png, pi77):
  return [[png.palette.colors[pi77[y][x]] for x in range(7)] for y in range(7)]


def rain77(c77):
  r77 = [[0 for x in range(7)] for y in range(7)]

  table = {
    (255, 255, 255):  -1, # 海岸境界
    (230, 230, 230):  -1, # 都道府県境界
    (255,   0,   0): 120,
    (255,   0, 255):  80,
    (255, 153,   0):  50,
    (255, 255,   0):  30,
    (  0, 255,   0):  20,
    (  0,   0, 255):  10, # 5-10mm/h
    ( 51, 102, 255):   5, # 1-5mm/h
    (153, 204, 255):   1, # 0-1mm/h
  }

  for y in range(7):
    for x in range(7):
      r77[y][x] = table.get(c77[y][x], 0)

  return r77

area  = 201
time  = nowcast.get_current_observed_time()
image = nowcast.get_image(area, time, 0)
png = png.Png8bitPalette.load(image)
print png

xy = (116,347)

pi77 = pindex77(png, xy)
print pi77
dump_matrix(pi77)

c77 = color77(png, pi77)
print c77

r77 = rain77(c77)
print r77
dump_matrix(r77)

ir77 = interpolate_rain77(r77)
print ir77
dump_matrix(ir77)

r55 = window55(ir77)
print r55
dump_matrix(r55)

w55 = (
  (0.6, 0.7, 0.8, 0.7, 0.6),
  (0.7, 0.8, 0.9, 0.8, 0.7),
  (0.8, 0.9, 1.0, 0.9, 0.8),
  (0.7, 0.8, 0.9, 0.8, 0.7),
  (0.6, 0.7, 0.8, 0.7, 0.6))
print weighted_average55(r55, w55)
