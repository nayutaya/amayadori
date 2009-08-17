# -*- coding: utf-8 -*-

import StringIO
import struct

import giflib



image = giflib.Image(10, 10, 8)

palette = image.palette
for i in xrange(256):
  palette.append((i, 0, 255 - i))

bitmap = image.bitmap
for y in range(10):
  for x in range(10):
    i = y * 10 + x
    bitmap.set_pixel(x, y, (i * 4) % 256)

f = open("tmp.gif", "wb")

blocks = image.create_blocks()
for block in blocks:
  block.write(f)


trailer = image.create_trailer()
trailer.write(f)

f.close()
