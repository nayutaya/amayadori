# -*- coding: utf-8 -*-

import re
import datetime
import logging
import StringIO
import struct
import binascii
import zlib
from google.appengine.ext import db
from google.appengine.api import urlfetch

import model
import png


def get_jst_now():
  return datetime.datetime.utcnow() + datetime.timedelta(hours = 9)

def get_per_minute_time(time):
  return datetime.datetime(time.year, time.month, time.day, time.hour, time.minute)

def get_current_observed_time():
  current_time = get_per_minute_time(get_jst_now())
  logging.info("current time: %s", current_time)

  caches = db.GqlQuery("SELECT * FROM ObservedTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    logging.info("cache hit")

    return caches[0].observed_time

  else:
    logging.info("cache miss")

    result = urlfetch.fetch("http://www.jma.go.jp/jp/radnowc/hisjs/radar.js")
    if result.status_code == 200:
      list = re.compile(r"\d{12}-\d{2}\.png").findall(result.content)
      list.sort()

      match = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})").match(list[-1])
      # TODO: if not match, raise exception

      observed_time = datetime.datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5)))

      cache = model.ObservedTimeCache(
        current_time  = current_time,
        observed_time = observed_time,
        expire_time   = current_time + datetime.timedelta(minutes = 20))
      cache.put()

      return observed_time
    #else:
      # TODO: raise exception

def get_current_predictive_time():
  current_time = get_per_minute_time(get_jst_now())
  logging.info("current time: %s", current_time)

  caches = db.GqlQuery("SELECT * FROM PredictiveTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    logging.info("cache hit")

    return caches[0].predictive_time

  else:
    logging.info("cache miss")

    result = urlfetch.fetch("http://www.jma.go.jp/jp/radnowc/hisjs/nowcast.js")
    if result.status_code == 200:
      list = re.compile(r"\d{12}-\d{2}\.png").findall(result.content)
      list.sort()

      match = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})").match(list[-1])
      # TODO: if not match, raise exception

      predictive_time = datetime.datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5)))

      cache = model.PredictiveTimeCache(
        current_time    = current_time,
        predictive_time = predictive_time,
        expire_time     = current_time + datetime.timedelta(minutes = 20))
      cache.put()

      return predictive_time
    #else:
      # TODO: raise exception

def create_observed_image_url(area, time):
  url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar/"
  url += str(area)
  url += "/"
  url += time.strftime("%Y%m%d%H%M")
  url += "-00.png"
  return url

def create_predictive_image_url(area, time, no):
  url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/"
  url += str(area)
  url += "/"
  url += time.strftime("%Y%m%d%H%M")
  url += "-"
  url += ("%02i" % no)
  url += ".png"
  return url

def create_image_url(area, time, no):
  if no == 0:
    return create_observed_image_url(area, time)
  else:
    return create_predictive_image_url(area, time, no)

def get_image(area, time, ordinal):
  logging.info("get_image")

  caches = db.GqlQuery("SELECT * FROM ImageCache WHERE area = :1 AND time = :2 AND ordinal = :3", area, time, ordinal)

  if caches.count() > 0:
    logging.info("cache hit")
    cache = caches[0]
  else:
    logging.info("cache miss")
    url = create_image_url(area, time, ordinal)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      cache = model.ImageCache(
        area        = area,
        time        = time,
        ordinal     = ordinal,
        image       = db.Blob(result.content),
        expire_time = get_jst_now() + datetime.timedelta(minutes = 20))
      cache.put()
    #else:

  return cache.image


#print get_current_observed_time()
#print get_current_predictive_time()
#print create_image_url(211, datetime.datetime.now(), 0)
#print create_image_url(211, datetime.datetime.now(), 1)

#print "Content-Type: image/png"
#print ""
#time = get_current_observed_time()
#print get_image(211, time, 0)
#time = get_current_predictive_time()
#print get_image(211, time, 1)

print "Content-Type: text/plain"
print ""

def unpack_long(bin):
  return struct.unpack("!L", bin)[0]

def unpack_byte(bin):
  return struct.unpack("B", bin)[0]



def read_all_chunks(io):
  chunks = png.Chunk.read_to_end(io)
  return [(chunk.type, chunk.data) for chunk in chunks]

def get_compressed_data(chunks):
  return "".join([data for (type, data) in chunks if type == "IDAT"])

def get_decompressed_data(chunks):
  return zlib.decompress(get_compressed_data(chunks))

def get_chunk_data(chunks, type):
  for (ctype, cdata) in chunks:
    if ctype == type:
      return cdata
  raise Exception, "chunk not found"


def get_header(chunks):
  header = get_chunk_data(chunks, "IHDR")
  io = StringIO.StringIO(header)
  return {
    "width"              : unpack_long(io.read(4)),
    "height"             : unpack_long(io.read(4)),
    "bit_depth"          : unpack_byte(io.read(1)),
    "colour_type"        : unpack_byte(io.read(1)),
    "compression_method" : unpack_byte(io.read(1)),
    "filter_method"      : unpack_byte(io.read(1)),
    "interlace_method"   : unpack_byte(io.read(1)),
  }


time  = get_current_observed_time()
image = get_image(211, time, 0)

io = StringIO.StringIO(image)
signature = png.Signature.read(io)
chunks = read_all_chunks(io)

header = get_header(chunks)
print header

data = get_decompressed_data(chunks)
print len(data)

print header["width"]
print header["height"]

dx = header["width"]
dy = header["height"]
if len(data) != (dx + 1) * dy:
  raise Exception, "invalid data"

io = StringIO.StringIO(data)

lines = []

for i in range(1, dy):
  filter = struct.unpack("B", io.read(1))[0]
  line   = struct.unpack(str(dx) + "B", io.read(dx))

  if filter != 0:
    raise Exception, "unsupported filter type"

  lines.append(list(line))

print lines




#palette_bin = get_chunk_data(chunks, "PLTE")
#print len(palette_bin)
#palette = png.Palette.load(palette_bin)
#print palette

#bin = palette.dump()
#print len(palette.colors)
#print len(palette_bin)
#print len(bin)
#if bin != palette_bin:
#  raise Exception, "hoge"

io = StringIO.StringIO(image)
signature = png.Signature.read(io)
chunks    = png.Chunk.read_to_end(io)
print chunks

header_chunk = [chunk for chunk in chunks if chunk.type == "IHDR"][0]
header = png.Header.load(header_chunk.data)
print header_chunk
print header

pal_chunk = [chunk for chunk in chunks if chunk.type == "PLTE"][0]
pal = png.Palette.load(pal_chunk.data)
print pal_chunk
print pal
