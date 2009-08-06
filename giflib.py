# -*- coding: utf-8 -*-

import struct

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
    self.width                      = 0 # pixel
    self.height                     = 0 # pixel
    self.color_resolution           = 8 # bits
    self.is_sorted_color_table      = False
    self.size_of_global_color_table = 0 # bits
    self.background_color_index     = 0
    self.pixel_aspect_ratio         = 0

  def flag(self):
    flag  = 0
    flag |= (self.has_global_color_table_flag()     << 7)
    flag |= (self.color_resolution_flag()           << 4)
    flag |= (self.is_sorted_color_table_flag()      << 3)
    flag |= (self.size_of_global_color_table_flag() << 0)
    return flag

  def has_global_color_table_flag(self):
    return 0 if self.size_of_global_color_table == 0 else 1

  def color_resolution_flag(self):
    return self.color_resolution - 1

  def is_sorted_color_table_flag(self):
    return 1 if self.is_sorted_color_table else 0

  def size_of_global_color_table_flag(self):
    if self.size_of_global_color_table == 0:
      return 0
    else:
      return self.size_of_global_color_table - 1

  def write(self, io):
    io.write(self.signature)
    io.write(struct.pack("H", self.width))
    io.write(struct.pack("H", self.height))
    io.write(struct.pack("B", self.flag()))
    io.write(struct.pack("B", self.background_color_index))
    io.write(struct.pack("B", self.pixel_aspect_ratio))
    return self

# 低レベル イメージブロックヘッダ
class RawImageBlockHeader:
  def __init__(self):
    self.left                  = 0 # pixel
    self.top                   = 0 # pixel
    self.width                 = 0 # pixel
    self.height                = 0 # pixel
    self.is_interlaced         = False
    self.is_sorted_color_table = False
    self.size_of_color_table   = 0 # bits
