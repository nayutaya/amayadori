# -*- coding: utf-8 -*-

import datetime
import logging
import StringIO
import struct
import binascii
import zlib

import nowcast
import png




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


time  = nowcast.get_current_observed_time()
image = nowcast.get_image(211, time, 0)


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

data_chunks = [chunk for chunk in chunks if chunk.type == "IDAT"]
data = "".join([chunk.data for chunk in data_chunks])
bitmap = png.BitmapFor8bitPalette.load(zlib.decompress(data), header.width, header.height)
print data_chunks
print len(data)
print len(zlib.decompress(data))
#for line in bitmap.bitmap:
#  print ",".join(["%02X" % x for x in line])

pngc = png.PngContainer.load(image)
print pngc
