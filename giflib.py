# -*- coding: utf-8 -*-

# 高レベル ビットマップクラス
class Bitmap:
  def __init__(self, width, height, depth = 8):
    self.width  = width
    self.height = height
    self.depth  = depth
    self.pixels = []

# 高レベル イメージクラス
#class Image:
#  def __init__(self, width, height):
#    self.palette = Palette()
#    self.bitmap  = Bitmap(width, height)

# 高レベル パレットクラス
#class Palette:
#  def __init__(self):
#    pass
