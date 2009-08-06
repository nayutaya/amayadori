# -*- coding: utf-8 -*-

import unittest

import giflib


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


if __name__ == "__main__":
  unittest.main()
