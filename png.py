# -*- coding: utf-8 -*-

import StringIO
import struct
import binascii

class Utility:
  @staticmethod
  def crc32(bin):
    return struct.unpack("!L", struct.pack("!l", binascii.crc32(bin)))[0]

class Chunk:
  def __init__(self, type, data = None):
    self.type = type
    self.data = data

  @staticmethod
  def read(io):
    length = struct.unpack("!L", io.read(4))[0]
    type   = io.read(4)
    data   = io.read(length)
    crc32  = struct.unpack("!L", io.read(4))[0]

    if crc32 != Utility.crc32(type + data):
      raise Exception, "CRC error"

    return Chunk(type = type, data = data)

  @staticmethod
  def read_to_end(io):
    chunks = []
    while True:
      chunk = Chunk.read(io)
      chunks.append(chunk)
      if chunk.type == "IEND":
        break
    return chunks

class Palette:
  def __init__(self, colors = []):
    self.colors = colors

  @staticmethod
  def load(bin):
    if len(bin) % 3 != 0:
      raise Exception, "invalid palette"

    io = StringIO.StringIO(bin)
    colors = []
    for i in range(0, len(bin) / 3):
      colors.append(struct.unpack("BBB", io.read(3)))
    return Palette(colors)

  def dump(self):
    if len(self.colors) > 256:
      raise "palette too big"

    bin = ""
    for color in self.colors:
      bin += struct.pack("BBB", *color)
    return bin
