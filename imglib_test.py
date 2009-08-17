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

  def test_set_pixels__invalid_size(self):
    obj = self.klass(10, 5)
    self.assertRaises(ValueError, obj.set_pixels, [0])

  def test_get_pixel(self):
    obj = self.klass(4, 3)
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
    obj = self.klass(4, 3)
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


class TestRgbBitmap(unittest.TestCase):
  def setUp(self):
    self.klass = imglib.RgbBitmap

  def test_init(self):
    obj = self.klass(10, 20)
    self.assertEqual(10, obj.width)
    self.assertEqual(20, obj.height)
    self.assertEqual(
      [(0, 0, 0) for i in xrange(10 * 20)],
      obj.pixels)

  def test_get_pixels(self):
    obj = self.klass(10, 5)
    self.assertEqual(
      [(0, 0, 0) for i in range(10 * 5)],
      obj.get_pixels())

  def test_set_pixels(self):
    pixels = [(i, 0, 0) for i in range(10 * 5)]
    obj = self.klass(10, 5)
    obj.set_pixels(pixels)
    self.assertEqual(pixels, obj.get_pixels())

  def test_set_pixels__invalid_size(self):
    obj = self.klass(10, 5)
    self.assertRaises(ValueError, obj.set_pixels, [(0, 0, 0)])

  def test_get_pixel(self):
    obj = self.klass(4, 3)
    obj.set_pixels([
      (1, 0, 0), (0, 0, 0), (0, 0, 0), (3, 0, 0),
      (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
      (4, 0, 0), (0, 0, 0), (0, 0, 0), (2, 0, 0),
    ])

    self.assertEqual((1, 0, 0), obj.get_pixel(0, 0))
    self.assertEqual((2, 0, 0), obj.get_pixel(3, 2))
    self.assertEqual((3, 0, 0), obj.get_pixel(3, 0))
    self.assertEqual((4, 0, 0), obj.get_pixel(0, 2))

  def test_set_pixel(self):
    obj = self.klass(4, 3)
    obj.set_pixel(0, 0, (1, 0, 0))
    obj.set_pixel(3, 2, (2, 0, 0))
    obj.set_pixel(3, 0, (3, 0, 0))
    obj.set_pixel(0, 2, (4, 0, 0))

    expected = [
      (1, 0, 0), (0, 0, 0), (0, 0, 0), (3, 0, 0),
      (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
      (4, 0, 0), (0, 0, 0), (0, 0, 0), (2, 0, 0),
    ]
    self.assertEqual(expected, obj.get_pixels())


if __name__ == "__main__":
  unittest.main()
