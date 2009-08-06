# -*- coding: utf-8 -*-

# 低レベルGIFライブラリ

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


# ファイルヘッダ
class FileHeader:
  def __init__(self):
    self.signature              = "GIF87a"
    self.width                  = 0 # pixel
    self.height                 = 0 # pixel
    self.color_resolution       = 8 # bits
    self.is_sorted_color_table  = False
    self.color_table_size       = 0 # bits
    self.background_color_index = 0
    self.pixel_aspect_ratio     = 0

  def has_color_table_flag(self):
    return 0 if self.color_table_size == 0 else 1

  def color_resolution_flag(self):
    return self.color_resolution - 1

  def is_sorted_color_table_flag(self):
    return 1 if self.is_sorted_color_table else 0

  def color_table_size_flag(self):
    if self.color_table_size == 0:
      return 0
    else:
      return self.color_table_size - 1

  def flag(self):
    flag  = 0
    flag |= (self.has_color_table_flag()       << 7)
    flag |= (self.color_resolution_flag()      << 4)
    flag |= (self.is_sorted_color_table_flag() << 3)
    flag |= (self.color_table_size_flag()      << 0)
    return flag

  def write(self, io):
    io.write(self.signature)
    io.write(struct.pack("H", self.width))
    io.write(struct.pack("H", self.height))
    io.write(struct.pack("B", self.flag()))
    io.write(struct.pack("B", self.background_color_index))
    io.write(struct.pack("B", self.pixel_aspect_ratio))
    return self


# イメージブロックヘッダ
class ImageBlockHeader:
  def __init__(self):
    self.left                  = 0 # pixel
    self.top                   = 0 # pixel
    self.width                 = 0 # pixel
    self.height                = 0 # pixel
    self.is_interlaced         = False
    self.is_sorted_color_table = False
    self.color_table_size      = 0 # bits

  def has_color_table_flag(self):
    return 0 if self.color_table_size == 0 else 1

  def is_interlaced_flag(self):
    return 1 if self.is_interlaced else 0

  def is_sorted_color_table_flag(self):
    return 1 if self.is_sorted_color_table else 0

  def color_table_size_flag(self):
    if self.color_table_size == 0:
      return 0
    else:
      return self.color_table_size - 1

  def flag(self):
    flag = 0
    flag |= (self.has_color_table_flag()       << 7)
    flag |= (self.is_interlaced_flag()         << 6)
    flag |= (self.is_sorted_color_table_flag() << 5)
    flag |= (self.color_table_size_flag()      << 0)
    return flag

  def write(self, io):
    io.write(struct.pack("B", 0x2c))
    io.write(struct.pack("H", self.left))
    io.write(struct.pack("H", self.top))
    io.write(struct.pack("H", self.width))
    io.write(struct.pack("H", self.height))
    io.write(struct.pack("B", self.flag()))
    return self


# トレーラー
class Trailer:
  def __init__(self):
    pass

  def write(self, io):
    io.write(struct.pack("B", 0x3b))
    return self


# カラーテーブル
# MEMO: ひとまず8bitカラー専用とする
class ColorTable:
  def __init__(self):
    self.table = []

  def size(self):
    return len(self.table)

  def bit_size(self):
    return 8

  def append(self, color):
    self.table.append(color)
    return self

  def write(self, io):
    count = 0
    max   = 2 ** self.bit_size()

    for (r, g, b) in self.table:
      io.write(struct.pack("BBB", r, g, b))
      count += 1

    for i in range(max - count):
      io.write(struct.pack("BBB", 0, 0, 0))

    return self

# 無圧縮イメージブロックデータ
# MEMO: ひとまず8bitカラー専用とする
class UncompressedImageBlockData:
  def __init__(self):
    self.pixels = []

  def size(self):
    return len(self.pixels)

  def append(self, pixel):
    self.pixels.append(pixel)
    return self

  def bitsets(self):
    bitsets = []

    count = 0
    for pixel in self.pixels:
      if count % 254 == 0:
        bitsets.append("100000000") # clear code

      bin = ""
      for i in range(8):
        bin = str(pixel & 1) + bin
        pixel >>= 1
      bitsets.append("0" + bin)
      count += 1

    if len(self.pixels) == 0:
      bitsets.append("100000000") # clear code

    bitsets.append("100000001") # end code
    return bitsets

  def bits_to_bytes(self, bits):
    bytes = []

    while len(bits) > 0:
      octet = bits[0:8]
      bits  = bits[8:]
      bytes.append(int(octet, 2))

    return bytes

  def bytes(self):
    bitsets = self.bitsets()
    bitsets.reverse()

    bits    = "".join(bitsets)
    padding = "".join(["0" for i in range(8 - (len(bits) % 8))]) if len(bits) % 8 > 0 else ""

    bytes = self.bits_to_bytes(padding + bits)
    bytes.reverse()

    return bytes


# イメージブロック
class ImageBlock:
  def __init__(self):
    self.minimum_code = 8 # bit
    self.data         = []

  def write(self, io):
    io.write(struct.pack("B", self.minimum_code))

    if len(self.data) > 0:
      io.write(struct.pack("B", len(self.data)))
      for byte in self.data:
        io.write(struct.pack("B", byte))

    # Block Terminator
    io.write(struct.pack("B", 0))

    return self
