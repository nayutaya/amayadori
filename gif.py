# -*- coding: utf-8 -*-

import StringIO
import struct

import giflib


f = open("tmp.gif", "wb")

image = giflib.Image(10, 10, 8)
blocks = image.create_blocks()
for block in blocks:
  block.write(f)

palette = giflib.Palette()
for i in xrange(256):
  palette.append((i, 0, 255 - i))
color_table = palette.create_color_table()
color_table.write(f)


bitmap = giflib.Bitmap(10, 10, 8)
for y in range(10):
  for x in range(10):
    i = y * 10 + x
    bitmap.set_pixel(x, y, (i * 4) % 256)


image_block = bitmap.create_image_block()
image_block.write(f)

trailer = image.create_trailer()
trailer.write(f)

f.close()
