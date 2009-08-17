# -*- coding: utf-8 -*-

import gifrawlib
import imglib


# 高レベル ビットマップクラス
class Bitmap:
  def __init__(self, width, height, depth = 8):
    self.bitmap = imglib.IndexBitmap(width, height)
    self.depth  = depth

  def width(self):
    return self.bitmap.width

  def height(self):
    return self.bitmap.height

  def get_pixels(self):
    return self.bitmap.get_pixels()

  def set_pixels(self, pixels):
    self.bitmap.set_pixels(pixels)
    return self

  def get_pixel(self, x, y):
    return self.bitmap.get_pixel(x, y)

  def set_pixel(self, x, y, pixel):
    self.bitmap.set_pixel(x, y, pixel)
    return self

  def create_image_block_data(self):
    data = gifrawlib.UncompressedImageBlockData()
    for pixel in self.get_pixels():
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
