# -*- coding: utf-8 -*-

import StringIO
import struct

import gifrawlib
import giflib

def write_image_block_header(io):
  header = gifrawlib.ImageBlockHeader()
  header.left                  = 0
  header.top                   = 0
  header.width                 = 10
  header.height                = 10
  header.is_interlaced         = False
  header.is_sorted_color_table = False
  header.color_table_size      = 8
  header.write(io)

def write_trailer(io):
  trailer = gifrawlib.Trailer()
  trailer.write(io)

f = open("tmp.gif", "wb")

image = giflib.Image(10, 10, 8)
file_header = image.create_file_header()
file_header.write(f)

write_image_block_header(f)

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

write_trailer(f)
f.close()
