# -*- coding: utf-8 -*-

import unittest
import StringIO

import ppmlib
import imglib


class TestPpmWriter(unittest.TestCase):
  def setUp(self):
    self.klass = ppmlib.PpmWriter

  def test_init(self):
    bitmap = imglib.RgbBitmap(10, 5)
    obj = self.klass(bitmap)
    self.assertEqual(bitmap, obj.bitmap)

  def test_write__minimum(self):
    sio = StringIO.StringIO()
    bitmap = imglib.RgbBitmap(1, 1)
    bitmap.set_pixel(0, 0, (1, 2, 3))
    obj = self.klass(bitmap)
    obj.write(sio)

    expected  = "P3\n"
    expected += "1 1\n"
    expected += "255\n"
    expected += "1 2 3\n"
    self.assertEqual(expected, sio.getvalue())

  def test_write__3x2(self):
    sio = StringIO.StringIO()
    bitmap = imglib.RgbBitmap(3, 2)
    bitmap.set_pixel(0, 0, (1, 2, 3))
    bitmap.set_pixel(1, 0, (4, 5, 6))
    bitmap.set_pixel(2, 0, (7, 8, 9))
    bitmap.set_pixel(0, 1, (10, 11, 12))
    bitmap.set_pixel(1, 1, (13, 14, 15))
    bitmap.set_pixel(2, 1, (16, 17, 18))
    obj = self.klass(bitmap)
    obj.write(sio)

    expected  = "P3\n"
    expected += "3 2\n"
    expected += "255\n"
    expected += "1 2 3 4 5 6 7 8 9\n"
    expected += "10 11 12 13 14 15 16 17 18\n"
    self.assertEqual(expected, sio.getvalue())

if __name__ == "__main__":
  unittest.main()
