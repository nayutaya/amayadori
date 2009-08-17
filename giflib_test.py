# -*- coding: utf-8 -*-

import unittest
import StringIO

import giflib
import gifrawlib


class TestBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.Bitmap(10, 20)
    self.assertEqual(10, obj.width())
    self.assertEqual(20, obj.height())
    self.assertEqual(8,  obj.depth())

  def test_get_pixel(self):
    obj = giflib.Bitmap(4, 3)
    obj.set_pixels([
      1, 0, 0, 3,
      0, 0, 0, 0,
      4, 0, 0, 2,
    ])

    self.assertEqual(1, obj.get_pixel(0, 0))
    self.assertEqual(2, obj.get_pixel(3, 2))
    self.assertEqual(3, obj.get_pixel(3, 0))
    self.assertEqual(4, obj.get_pixel(0, 2))

  def test_set_pixel(self):
    obj = giflib.Bitmap(4, 3)
    obj.set_pixel(0, 0, 1)
    obj.set_pixel(3, 2, 2)
    obj.set_pixel(3, 0, 3)
    obj.set_pixel(0, 2, 4)

    expected = [
      1, 0, 0, 3,
      0, 0, 0, 0,
      4, 0, 0, 2,
    ]
    self.assertEqual(expected, obj.get_pixels())

  def test_create_image_block_data(self):
    obj = giflib.Bitmap(3, 2)
    obj.set_pixels([0, 1, 2, 3, 4, 5])

    ibd = gifrawlib.UncompressedImageBlockData()
    for byte in obj.get_pixels():
      ibd.append(byte)
    self.assertEqual(
      ibd.bytes(),
      obj.create_image_block_data().bytes())

  def test_create_image_block(self):
    obj = giflib.Bitmap(3, 2)
    obj.set_pixels([0, 1, 2, 3, 4, 5])

    bytes = obj.create_image_block_data().bytes()

    ib = obj.create_image_block()
    self.assertEqual(8,     ib.minimum_code)
    self.assertEqual(bytes, ib.data)


class PaletteBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.Palette()
    self.assertEqual(8, obj.depth())

    obj = giflib.Palette(2)
    self.assertEqual(2, obj.depth())

  def test_size(self):
    obj = giflib.Palette()
    self.assertEqual(0, obj.size())

  def test_append(self):
    obj = giflib.Palette()
    self.assertEqual(0, obj.size())
    self.assertEqual(0, obj.append((0, 0, 0)))
    self.assertEqual(1, obj.size())
    self.assertEqual(1, obj.append((0, 0, 0)))
    self.assertEqual(2, obj.size())

  def test_get_colors(self):
    obj = giflib.Palette()
    self.assertEqual(
      [],
      obj.get_colors())

    obj.append((1, 2, 3))
    self.assertEqual(
      [(1, 2, 3)],
      obj.get_colors())

  def test_create_color_table__empty(self):
    ct1 = gifrawlib.ColorTable()

    obj = giflib.Palette()
    ct2 = obj.create_color_table()

    self.assertEqual(ct1.get_colors(), ct2.get_colors())

  def test_create_color_table__not_empty(self):
    ct1 = gifrawlib.ColorTable()
    ct1.append((1, 2, 3))

    obj = giflib.Palette()
    obj.append((1, 2, 3))
    ct2 = obj.create_color_table()

    self.assertEqual(ct1.get_colors(), ct2.get_colors())


class ImageBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init__case1(self):
    obj = giflib.Image(1, 2)
    self.assertEqual(1, obj.width())
    self.assertEqual(2, obj.height())
    self.assertEqual(8, obj.depth())
    self.assertEqual(1, obj.bitmap.width())
    self.assertEqual(2, obj.bitmap.height())
    self.assertEqual(8, obj.bitmap.depth())
    self.assertEqual(8, obj.palette.depth())

  def test_init__case2(self):
    obj = giflib.Image(10, 20, 2)
    self.assertEqual(10, obj.width())
    self.assertEqual(20, obj.height())
    self.assertEqual(2,  obj.depth())

  def test_create_file_header(self):
    obj = giflib.Image(10, 20, 8)
    fh = obj.create_file_header()
    self.assertEqual(gifrawlib.FileHeader, fh.__class__)
    self.assertEqual(10,    fh.width)
    self.assertEqual(20,    fh.height)
    self.assertEqual(8,     fh.color_resolution)
    self.assertEqual(False, fh.is_sorted_color_table)
    self.assertEqual(0,     fh.color_table_size)
    self.assertEqual(0,     fh.background_color_index)
    self.assertEqual(0,     fh.pixel_aspect_ratio)

  def test_create_image_block_header(self):
    obj = giflib.Image(10, 20, 8)
    ibh = obj.create_image_block_header()
    self.assertEqual(gifrawlib.ImageBlockHeader, ibh.__class__)
    self.assertEqual(0,     ibh.left)
    self.assertEqual(0,     ibh.top)
    self.assertEqual(10,    ibh.width)
    self.assertEqual(20,    ibh.height)
    self.assertEqual(False, ibh.is_interlaced)
    self.assertEqual(False, ibh.is_sorted_color_table)
    self.assertEqual(8,     ibh.color_table_size)

  def test_create_trailer(self):
    obj = giflib.Image(10, 20, 8)
    t = obj.create_trailer()
    self.assertEqual(gifrawlib.Trailer, t.__class__)

  def test_create_blocks(self):
    obj = giflib.Image(10, 20, 8)
    obj.palette.append((1, 2, 3))

    blocks = obj.create_blocks()
    self.assertEqual(5, len(blocks))

    self.assertEqual(
      gifrawlib.FileHeader,
      blocks[0].__class__)
    self.assertEqual(10, blocks[0].width)
    self.assertEqual(20, blocks[0].height)

    self.assertEqual(
      gifrawlib.ImageBlockHeader,
      blocks[1].__class__)
    self.assertEqual(10, blocks[1].width)
    self.assertEqual(20, blocks[1].height)

    self.assertEqual(
      gifrawlib.ColorTable,
      blocks[2].__class__)
    self.assertEqual(
      [(1, 2, 3)],
      blocks[2].get_colors())

    self.assertEqual(
      gifrawlib.ImageBlock,
      blocks[3].__class__)
    self.assertEqual(
      obj.bitmap.create_image_block().data,
      blocks[3].data)

    self.assertEqual(
      gifrawlib.Trailer,
      blocks[4].__class__)

  def test_wirte(self):
    obj = giflib.Image(10, 20, 8)
    sio1 = StringIO.StringIO()
    sio2 = StringIO.StringIO()

    for block in obj.create_blocks():
      block.write(sio1)

    obj.write(sio2)

    self.assertEqual(sio1.getvalue(), sio2.getvalue())


if __name__ == "__main__":
  unittest.main()
