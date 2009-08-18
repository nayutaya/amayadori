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

class TestColor(unittest.TestCase):
  def setUp(self):
    self.klass = imglib.Color

  def test_rgb_to_int(self):
    self.assertEqual(0x000000, self.klass.rgb_to_int((  0,   0,   0)))
    self.assertEqual(0xFF0000, self.klass.rgb_to_int((255,   0,   0)))
    self.assertEqual(0x00FF00, self.klass.rgb_to_int((  0, 255,   0)))
    self.assertEqual(0x0000FF, self.klass.rgb_to_int((  0,   0, 255)))
    self.assertEqual(0xFFFFFF, self.klass.rgb_to_int((255, 255, 255)))

  def test_int_to_rgb(self):
    self.assertEqual((  0,   0,   0), self.klass.int_to_rgb(0x000000))
    self.assertEqual((255,   0,   0), self.klass.int_to_rgb(0xFF0000))
    self.assertEqual((  0, 255,   0), self.klass.int_to_rgb(0x00FF00))
    self.assertEqual((  0,   0, 255), self.klass.int_to_rgb(0x0000FF))
    self.assertEqual((255, 255, 255), self.klass.int_to_rgb(0xFFFFFF))


if __name__ == "__main__":
  unittest.main()
