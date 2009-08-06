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

  def test_flag(self):
    obj = giflib.RawHeader()

    obj.color_resolution           = 1
    obj.is_sorted_color_table      = False
    obj.size_of_global_color_table = 0
    self.assertEqual(int("00000000", 2), obj.flag())

    #obj.color_resolution           = 2
    #obj.is_sorted_color_table      = False
    #obj.size_of_global_color_table = 0
    #self.assertEqual(int("00010000", 2), obj.flag())

  def test_has_global_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.size_of_global_color_table = 0
    self.assertEqual(0, obj.has_global_color_table_flag())
    obj.size_of_global_color_table = 1
    self.assertEqual(1, obj.has_global_color_table_flag())
    obj.size_of_global_color_table = 8
    self.assertEqual(1, obj.has_global_color_table_flag())

  def test_color_resolution_flag(self):
    obj = giflib.RawHeader()
    obj.color_resolution = 1
    self.assertEqual(0, obj.color_resolution_flag())
    obj.color_resolution = 8
    self.assertEqual(7, obj.color_resolution_flag())

  def test_is_sorted_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.is_sorted_color_table = False
    self.assertEqual(0, obj.is_sorted_color_table_flag())
    obj.is_sorted_color_table = True
    self.assertEqual(1, obj.is_sorted_color_table_flag())

  def test_size_of_global_color_table_flag(self):
    obj = giflib.RawHeader()
    obj.size_of_global_color_table = 0
    self.assertEqual(0, obj.size_of_global_color_table_flag())
    obj.size_of_global_color_table = 1
    self.assertEqual(0, obj.size_of_global_color_table_flag())
    obj.size_of_global_color_table = 8
    self.assertEqual(7, obj.size_of_global_color_table_flag())

if __name__ == "__main__":
  unittest.main()
