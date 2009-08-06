# -*- coding: utf-8 -*-

# 高レベル ビットマップクラス
class Bitmap:
  def __init__(self, width, height, depth = 8):
    self.width  = width
    self.height = height
    self.depth  = depth
    self.pixels = [0 for i in xrange(self.width * self.height)]

  def get_pixel(self, x, y):
    return self.pixels[y * self.width + x]

  def set_pixel(self, x, y, pixel):
    self.pixels[y * self.width + x] = pixel
    return self

# 高レベル イメージクラス
#class Image:
#  def __init__(self, width, height):
#    self.palette = Palette()
#    self.bitmap  = Bitmap(width, height)

# 高レベル パレットクラス
#class Palette:
#  def __init__(self):
#    pass
