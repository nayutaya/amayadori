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

if __name__ == "__main__":
  unittest.main()
