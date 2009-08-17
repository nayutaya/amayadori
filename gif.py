# -*- coding: utf-8 -*-

import StringIO
import struct

import giflib


image = giflib.Image(10, 10, 8)

for i in xrange(256):
  image.append_color((i, 0, 255 - i))

for y in range(10):
  for x in range(10):
    i = y * 10 + x
    image.set_pixel((x, y), (i * 4) % 256)

f = open("tmp.gif", "wb")
image.write(f)
f.close()
