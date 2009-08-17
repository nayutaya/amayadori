# -*- coding: utf-8 -*-

import unittest

import giflib
import gifrawlib


class TestBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.Bitmap(10, 20)
    self.assertEqual(10, obj.width())
    self.assertEqual(20, obj.height())
    self.assertEqual(8,  obj.depth)

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
    self.assertEqual(8, obj.depth)

    obj = giflib.Palette(2)
    self.assertEqual(2, obj.depth)

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


if __name__ == "__main__":
  unittest.main()
