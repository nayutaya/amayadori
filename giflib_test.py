# -*- coding: utf-8 -*-

import unittest

import giflib

class TestRawHeader(unittest.TestCase):
  def setUp(self):
    pass

  def test_init(self):
    obj = giflib.RawHeader()
    self.assertEqual("GIF87a", obj.signature)
    self.assertEqual(None,     obj.width)
    self.assertEqual(None,     obj.height)
    self.assertEqual(8,        obj.color_resolution)
    self.assertEqual(False,    obj.is_sorted_color_table)
    self.assertEqual(0,        obj.size_of_global_color_table)

if __name__ == "__main__":
  unittest.main()
