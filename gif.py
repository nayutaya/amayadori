# -*- coding: utf-8 -*-

import StringIO
import struct

import giflib


image = giflib.Image(16, 16, 8)

for i in xrange(256):
  image.append_color((i, i * 4 % 256, 255 - (i * 2 % 256)))

for y in range(16):
  for x in range(16):
    i = y * 16 + x
    image.set_pixel((x, y), i % 256)

f = open("tmp.gif", "wb")
image.write(f)
f.close()
