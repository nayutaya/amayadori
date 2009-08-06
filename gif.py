# -*- coding: utf-8 -*-

import StringIO
import struct

import giflib

def write_header(io):
  header = giflib.RawHeader()
  header.width                      = 10
  header.height                     = 10
  header.color_resolution           = 8
  header.is_sorted_color_table      = False
  header.size_of_global_color_table = 0
  header.background_color_index     = 0
  header.pixel_aspect_ratio         = 0
  header.write(io)

def write_image_block_header(io):
  # Image Separator
  io.write(struct.pack("B", 0x2c))
  # Image Left Position
  io.write(struct.pack("H", 0))
  # Image Top Position
  io.write(struct.pack("H", 0))
  # Image Width
  width, height = 10, 10
  io.write(struct.pack("H", width))
  io.write(struct.pack("H", height))
  # Local Color Table Flag: あり
  # Interlace Flag: なし
  # Sort Flag: ソートなし
  # Reserved
  # Size of Local Color Table: 8bit
  io.write(struct.pack("B", int("10000111", 2)))

def write_local_color_table(io):
  for i in xrange(256):
    f.write(struct.pack("B", i))
    f.write(struct.pack("B", 0))
    f.write(struct.pack("B", 255 - i))

def write_trailer(io):
  io.write(struct.pack("B", 0x3b))

f = open("tmp.gif", "wb")
write_header(f)
write_image_block_header(f)
write_local_color_table(f)

def byte2binstr(value):
  bin = ""
  for i in range(8):
    bin = str(value & 1) + bin
    value = value >> 1
  return bin

pixels  = [(i * 4) % 256 for i in xrange(10 * 10)]
pixels2 = [byte2binstr(p) for p in pixels]
pixels3 = ["0" + x for x in pixels2]
print pixels

bits2 = []
bits2.append("100000000") # clear code
for x in pixels3:
  bits2.append(x)
bits2.append("100000001") # end code
bits2.reverse()

bits = "".join(bits2)
bits = "".join(["0" for i in range(8 - (len(bits) - (len(bits) / 8 * 8)))]) + bits # padding

bytes = []
while len(bits) > 0:
  oct  = bits[0:8]
  bits = bits[8:]
  bytes.append(int(oct, 2))
print bytes
print len(bytes)
bytes.reverse()

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
