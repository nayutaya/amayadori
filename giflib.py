# -*- coding: utf-8 -*-

import gifrawlib
import imglib


# 高レベル ビットマップクラス
class Bitmap:
  def __init__(self, width, height, depth = 8):
    self.bitmap = imglib.IndexBitmap(width, height)
    self.depth_ = depth

  def width(self):
    return self.bitmap.width

  def height(self):
    return self.bitmap.height

  def depth(self):
    return self.depth_

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
    return data

  def create_image_block(self):
    image_block_data = self.create_image_block_data()

    image_block = gifrawlib.ImageBlock();
    image_block.minimum_code = self.depth()
    image_block.data         = image_block_data.bytes()
    return image_block



# 高レベル パレットクラス
class Palette:
  def __init__(self, depth = 8):
    self.depth_ = depth
    self.colors = []

  def depth(self):
    return self.depth_

  def size(self):
    return len(self.colors)

  def append(self, rgb):
    self.colors.append(rgb)
    return self.size() - 1

  def get_colors(self):
    return self.colors[:]

  def create_color_table(self):
    color_table = gifrawlib.ColorTable()
    for color in self.colors:
      color_table.append(color)
    return color_table


# 高レベル イメージクラス
class Image:
  def __init__(self, width, height, depth = 8):
    self.palette = Palette(depth)
    self.bitmap  = Bitmap(width, height, depth)

  def width(self):
    return self.bitmap.width()

  def height(self):
    return self.bitmap.height()

  def depth(self):
    return self.bitmap.depth()

  def create_file_header(self):
    file_header = gifrawlib.FileHeader()
    file_header.width            = self.width()
    file_header.height           = self.height()
    file_header.color_resolution = self.depth()
    return file_header

  def create_image_block_header(self):
    image_block_header = gifrawlib.ImageBlockHeader()
    image_block_header.left             = 0
    image_block_header.top              = 0
    image_block_header.width            = self.width()
    image_block_header.height           = self.height()
    image_block_header.color_table_size = self.depth()
    return image_block_header

  def create_trailer(self):
    trailer = gifrawlib.Trailer()
    return trailer

  def create_blocks(self):
    blocks = []
    blocks.append(self.create_file_header())
    blocks.append(self.create_image_block_header())
    blocks.append(self.palette.create_color_table())
    return blocks
