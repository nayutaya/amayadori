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


if __name__ == "__main__":
  # 256x256のPPMイメージファイルを書き込む
  bitmap = imglib.RgbBitmap(256, 256)
  for y in range(256):
    for x in range(256):
      bitmap.set_pixel(x, y, (y, 0, x))
  file = open("tmp.ppm", "wb")
  ppm = PpmWriter(bitmap)
  ppm.write(file)
  file.close()
