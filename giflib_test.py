# -*- coding: utf-8 -*-

import unittest

import giflib
import gifrawlib


class TestBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.Bitmap(10, 20)
    self.assertEqual(10, obj.width)
    self.assertEqual(20, obj.height)
    self.assertEqual(8,  obj.depth)
    self.assertEqual(
      [0 for i in xrange(10 * 20)],
      obj.pixels)

  def test_get_pixel(self):
    obj = giflib.Bitmap(5, 4)
    obj.pixels = [
      1, 0, 0, 0, 3,
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      4, 0, 0, 0, 2,
    ]

    self.assertEqual(1, obj.get_pixel(0, 0))
    self.assertEqual(2, obj.get_pixel(4, 3))
    self.assertEqual(3, obj.get_pixel(4, 0))
    self.assertEqual(4, obj.get_pixel(0, 3))

  def test_set_pixel(self):
    obj = giflib.Bitmap(5, 4)
    obj.set_pixel(0, 0, 1)
    obj.set_pixel(4, 3, 2)
    obj.set_pixel(4, 0, 3)
    obj.set_pixel(0, 3, 4)

    expected = [
      1, 0, 0, 0, 3,
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      4, 0, 0, 0, 2,
    ]
    self.assertEqual(expected, obj.pixels)

  def test_create_image_block_data(self):
    obj = giflib.Bitmap(3, 2)
    obj.pixels = [0, 1, 2, 3, 4, 5]

    data = gifrawlib.UncompressedImageBlockData()
    for byte in obj.pixels:
      data.append(byte)
    expected = data.bytes()
    self.assertEqual(expected, obj.create_image_block_data())


if __name__ == "__main__":
  unittest.main()
