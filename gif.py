# -*- coding: utf-8 -*-

import StringIO
import struct

import gifrawlib

def write_header(io):
  header = gifrawlib.FileHeader()
  header.width                  = 10
  header.height                 = 10
  header.color_resolution       = 8
  header.is_sorted_color_table  = False
  header.color_table_size       = 0
  header.background_color_index = 0
  header.pixel_aspect_ratio     = 0
  header.write(io)

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

def write_local_color_table(io):
  ctable = gifrawlib.ColorTable()
  for i in xrange(256):
    ctable.append((i, 0, 255 - i))
  ctable.write(io)

def write_trailer(io):
  trailer = gifrawlib.Trailer()
  trailer.write(io)

f = open("tmp.gif", "wb")
write_header(f)
write_image_block_header(f)
write_local_color_table(f)

data = gifrawlib.UncompressedImageBlockData()
for i in xrange(10 * 10):
  data.append((i * 4) % 256)
bytes = data.bytes()

io = f
# LZW Minimum Code Side: 8bit
io.write(struct.pack("B", 8))

# Block Size: n
io.write(struct.pack("B", len(bytes)))

# Image Data:
for c in bytes:
  io.write(struct.pack("B", c))

# Block Terminator: 0
io.write(struct.pack("B", 0))

write_trailer(f)
f.close()
