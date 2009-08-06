# -*- coding: utf-8 -*-

# 高レベル イメージクラス
class Image:
  def __init__(self):
    pass

# 高レベル パレットクラス
class Palette:
  def __init__(self):
    pass

# 高レベル ビットマップクラス
class Bitmap:
  def __init__(self):
    pass

# 低レベル GIFヘッダ
class RawHeader:
  def __init__(self):
    self.signature                  = "GIF87a"
    self.width                      = None
    self.height                     = None
    self.color_resolution           = 8
    self.is_sorted_color_table      = False
    self.size_of_global_color_table = 0
