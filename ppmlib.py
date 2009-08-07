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

    r, g, b = self.bitmap.get_pixel(0, 0)
    io.write(str(r) + " " + str(g) + " " + str(b))
    io.write("\n")

    return self
