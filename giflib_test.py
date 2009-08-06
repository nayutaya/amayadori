# -*- coding: utf-8 -*-

import unittest

import giflib


class TestBitmap(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.Bitmap(1, 2)
    self.assertEqual(1,  obj.width)
    self.assertEqual(2,  obj.height)
    self.assertEqual(8,  obj.depth)
    self.assertEqual([], obj.pixels)

if __name__ == "__main__":
  unittest.main()
