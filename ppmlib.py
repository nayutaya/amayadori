# -*- coding: utf-8 -*-

import imglib

# ASCII形式PPMファイル書き込みクラス
class PpmWriter:
  def __init__(self, bitmap):
    self.bitmap = bitmap

  def write(self, io):
    io.write("P3\n")
    io.write(str(self.bitmap.width))
    io.write(" ")
    io.write(str(self.bitmap.height))
    io.write("\n")
    io.write("255\n")

    for y in xrange(self.bitmap.height):
      line = []
      for x in xrange(self.bitmap.width):
        r, g, b = self.bitmap.get_pixel(x, y)
        line.append(str(r) + " " + str(g) + " " + str(b))
      io.write(" ".join(line))
      io.write("\n")

    return self
