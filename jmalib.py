# -*- coding: utf-8 -*-

import datetime
import re

import imglib


color_reduction_table = {
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
  (102, 102, 102): (102, 102, 102), # ŠCŠÝ‹«ŠE/ƒOƒŠƒbƒh
  (255, 255, 255): (255, 255, 255), # ŠCŠÝ‹«ŠE
  (116, 123, 114): (116, 123, 114), # ŠCŠÝ‹«ŠE
  (160, 160, 160): (160, 160, 160), # ŠCŠÝ‹«ŠE
}

railfall_table = {
  (255,   0,   0): (80, 100),
  (255,   0, 255): (50,  80),
  (255, 153,   0): (30,  50),
  (255, 255,   0): (20,  30),
  (  0, 255,   0): (10,  20),
  (  0,   0, 255): ( 5,  10),
  ( 51, 102, 255): ( 1,   5),
  (153, 204, 255): ( 0,   1),
}


def parse_radar_js(src):
  regexp = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})-(\d{2})\.png")
  result = []

  for (year, month, day, hour, minute, ordinal) in regexp.findall(src):
    time = datetime.datetime(
      int(year), int(month), int(day),
      int(hour), int(minute))
    result.append((time, int(ordinal)))

  return result

def parse_nowcast_js(src):
  regexp = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})-(\d{2})\.png")
  result = []

  for (year, month, day, hour, minute, ordinal) in regexp.findall(src):
    time = datetime.datetime(
      int(year), int(month), int(day),
      int(hour), int(minute))
    result.append((time, int(ordinal)))

  return result

def get_latest_time(time_and_ordinals):
  times = [time for (time, ordinal) in time_and_ordinals]
  times.sort()
  return times[-1]

def get_current_radar_time(fetcher):
  url    = "http://www.jma.go.jp/jp/radnowc/hisjs/radar.js"
  source = fetcher(url)
  parsed = parse_radar_js(source)
  return get_latest_time(parsed)

def get_current_nowcast_time(fetcher):
  url    = "http://www.jma.go.jp/jp/radnowc/hisjs/nowcast.js"
  source = fetcher(url)
  parsed = parse_nowcast_js(source)
  return get_latest_time(parsed)

def create_radar_image_url(area, time):
  url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar"
  url += "/" + ("%03i" % area)
  url += "/" + time.strftime("%Y%m%d%H%M")
  url += "-00.png"
  return url

def create_nowcast_image_url(area, time, ordinal):
  url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast"
  url += "/" + ("%03i" % area)
  url += "/" + time.strftime("%Y%m%d%H%M")
  url += "-" + ("%02i" % ordinal)
  url += ".png"
  return url

def create_image_url(area, time, ordinal):
  if ordinal == 0:
    return create_radar_image_url(area, time)
  else:
    return create_nowcast_image_url(area, time, ordinal)

def get_image(area, time, ordinal, fetcher):
  url    = create_image_url(area, time, ordinal)
  binary = fetcher(url)
  return binary

def is_water_color(rgb):
  if   rgb == (192, 192, 192): return True
  elif rgb == (193, 193, 193): return True
  else:
    r, g, b = rgb
    return (b >= g)

def is_ground_color(rgb):
  r, g, b = rgb
  return (g > b)

def color_reduction(rgb):
  ret = color_reduction_table.get(rgb)
  if ret == None:
    if is_ground_color(rgb):
      return ( 96, 128,  96)
    elif is_water_color(rgb):
      return ( 64,  96, 128)
    else:
      return (192,   0, 192)
  else:
    return ret

def get_minimum_rainfall_from_rgb(rgb):
  return railfall_table.get(rgb, (0, 0))[0]

def get_maximum_rainfall_from_rgb(rgb):
  return railfall_table.get(rgb, (0, 0))[1]

def get_rainfall_from_bitmap(bitmap):
  minimums = []
  maximums = []
  for pixel in bitmap.get_pixels():
    minimums.append(get_minimum_rainfall_from_rgb(pixel))
    maximums.append(get_maximum_rainfall_from_rgb(pixel))

  return (min(minimums), max(maximums))
