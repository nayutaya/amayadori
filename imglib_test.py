# -*- coding: utf-8 -*-

import unittest

import imglib


class TestIndexBitmap(unittest.TestCase):
  def setUp(self):
    self.klass = imglib.IndexBitmap

  def test_init(self):
    obj = self.klass(10, 20)
    self.assertEqual(10, obj.width)
    self.assertEqual(20, obj.height)
    self.assertEqual(
      [0 for i in xrange(10 * 20)],
      obj.pixels)

  def test_get_pixels(self):
    obj = self.klass(10, 5)
    self.assertEqual(
      [0 for i in range(10 * 5)],
      obj.get_pixels())

  def test_set_pixels(self):
    pixels = [i for i in range(10 * 5)]
    obj = self.klass(10, 5)
    obj.set_pixels(pixels)
    self.assertEqual(pixels, obj.get_pixels())


if __name__ == "__main__":
  unittest.main()
