# -*- coding: utf-8 -*-

import unittest

import ppmlib
import imglib


class TestPpmWriter(unittest.TestCase):
  def setUp(self):
    self.klass = ppmlib.PpmWriter

  def test_init(self):
    bitmap = imglib.RgbBitmap(10, 5)
    obj = self.klass(bitmap)
    self.assertEqual(bitmap, obj.bitmap)

if __name__ == "__main__":
  unittest.main()
