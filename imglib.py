# -*- coding: utf-8 -*-

# 汎用イメージライブラリ

# インデックスカラービットマップ
class IndexBitmap:
  def __init__(self, width, height):
    self.width  = width
    self.height = height
    self.pixels = [0 for i in xrange(self.width * self.height)]

  def get_pixels(self):
    return self.pixels[:]

  def set_pixels(self, pixels):
    if len(pixels) != self.width * self.height:
      raise ValueError, "invalid size"
    self.pixels = pixels[:]
    return self

  def get_pixel(self, x, y):
    return self.pixels[y * self.width + x]

  def set_pixel(self, x, y, pixel):
    self.pixels[y * self.width + x] = pixel
    return self


# RGBカラービットマップ
class RgbBitmap:
  def __init__(self, width, height):
    init_pixel = (0, 0, 0)

    self.width  = width
    self.height = height
    self.pixels = [init_pixel for i in xrange(self.width * self.height)]

  def get_pixels(self):
    return self.pixels[:]

  def set_pixels(self, pixels):
    if len(pixels) != self.width * self.height:
      raise ValueError, "invalid size"
    self.pixels = pixels[:]
    return self

  def get_pixel(self, x, y):
    return self.pixels[y * self.width + x]

  def set_pixel(self, x, y, pixel):
    self.pixels[y * self.width + x] = pixel
    return self
