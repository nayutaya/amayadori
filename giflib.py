# -*- coding: utf-8 -*-

import gifrawlib


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

  def create_image_block_data(self):
    data = gifrawlib.UncompressedImageBlockData()
    for pixel in self.pixels:
      data.append(pixel)
    return data.bytes()


# 高レベル イメージクラス
#class Image:
#  def __init__(self, width, height):
#    self.palette = Palette()
#    self.bitmap  = Bitmap(width, height)

# 高レベル パレットクラス
#class Palette:
#  def __init__(self):
#    pass
