# -*- coding: utf-8 -*-

import StringIO
import struct

class Palette:
  def __init__(self, colors = []):
    self.colors = colors

  @staticmethod
  def load(bin):
    if len(bin) % 3 != 0:
      raise Exception, "invalid palette"
    io = StringIO.StringIO(bin)
    colors = []
    for i in range(1, len(bin) / 3):
      colors.append(struct.unpack("BBB", io.read(3)))
    return Palette(colors)
