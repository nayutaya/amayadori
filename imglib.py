# -*- coding: utf-8 -*-

# 汎用イメージライブラリ

# ビットマップ基底クラス
class BitmapBase:
  def __init__(self, width, height, init_pixel):
    self.width  = width
    self.height = height
    self.pixels = [init_pixel for i in xrange(self.width * self.height)]

# インデックスカラービットマップクラス
class IndexBitmap(BitmapBase):
  def __init__(self, width, height):
    BitmapBase.__init__(self, width, height, 0)

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


# RGBカラービットマップクラス
class RgbBitmap(BitmapBase):
  def __init__(self, width, height):
    BitmapBase.__init__(self, width, height, (0, 0, 0))

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
