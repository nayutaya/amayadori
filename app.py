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


pngc = png.PngContainer.load(image)
print pngc
print pngc.chunks

header_chunk = pngc.first_chunk_by_type("IHDR")
header = png.Header.load(header_chunk.data)
print header_chunk
print header

pal_chunk = pngc.first_chunk_by_type("PLTE")
pal = png.Palette.load(pal_chunk.data)
print pal_chunk
print pal

data_chunk = pngc.joined_chunk_by_type("IDAT")
bitmap = png.BitmapFor8bitPalette.load(zlib.decompress(data_chunk.data), header.width, header.height)
print data_chunk
print len(data_chunk.data)
print len(zlib.decompress(data_chunk.data))
#for line in bitmap.bitmap:
#  print ",".join(["%02X" % x for x in line])
