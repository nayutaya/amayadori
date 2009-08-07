# -*- coding: utf-8 -*-

# 汎用イメージライブラリ

class IndexBitmap:
  def __init__(self, width, height):
    self.width  = width
    self.height = height
    self.pixels = [0 for i in xrange(self.width * self.height)]

  def get_pixels(self):
    return self.pixels[:]

  def set_pixels(self, pixels):
    self.pixels = pixels[:]
    return self
