# -*- coding: utf-8 -*-

import StringIO
import struct

def write_header(io):
  # Signature, Version
  io.write("GIF87a")
  # Logical Screen Width, Logical Screen Height
  width, height = 10, 5
  io.write(struct.pack("HH", width, height))
  # Global Color Table: なし
  # Color Resolution: 8bit
  # Sort Flag: ソートなし
  # Size of Global Color Table: 0bit
  flags = int("01110000", 2)
  io.write(struct.pack("B", flags))
  # Background Color Index
  io.write(struct.pack("B", 0))
  # Pixel Aspect Ratio
  io.write(struct.pack("B", 0))
  # Global Color Table: なし

f = open("tmp.gif", "wb")
write_header(f)
f.close()
