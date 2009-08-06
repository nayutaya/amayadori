# -*- coding: utf-8 -*-

import unittest
import StringIO

import gifrawlib


class TestFileHeader(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.FileHeader()

  def test_init(self):
    self.assertEqual("GIF87a", self.obj.signature)
    self.assertEqual(0,        self.obj.width)
    self.assertEqual(0,        self.obj.height)
    self.assertEqual(8,        self.obj.color_resolution)
    self.assertEqual(False,    self.obj.is_sorted_color_table)
    self.assertEqual(0,        self.obj.color_table_size)
    self.assertEqual(0,        self.obj.background_color_index)
    self.assertEqual(0,        self.obj.pixel_aspect_ratio)

  def test_has_color_table_flag(self):
    self.obj.color_table_size = 0
    self.assertEqual(0, self.obj.has_color_table_flag())
    self.obj.color_table_size = 1
    self.assertEqual(1, self.obj.has_color_table_flag())
    self.obj.color_table_size = 8
    self.assertEqual(1, self.obj.has_color_table_flag())

  def test_color_resolution_flag(self):
    self.obj.color_resolution = 1
    self.assertEqual(0, self.obj.color_resolution_flag())
    self.obj.color_resolution = 8
    self.assertEqual(7, self.obj.color_resolution_flag())

  def test_is_sorted_color_table_flag(self):
    self.obj.is_sorted_color_table = False
    self.assertEqual(0, self.obj.is_sorted_color_table_flag())
    self.obj.is_sorted_color_table = True
    self.assertEqual(1, self.obj.is_sorted_color_table_flag())

  def test_color_table_size_flag(self):
    self.obj.color_table_size = 0
    self.assertEqual(0, self.obj.color_table_size_flag())
    self.obj.color_table_size = 1
    self.assertEqual(0, self.obj.color_table_size_flag())
    self.obj.color_table_size = 8
    self.assertEqual(7, self.obj.color_table_size_flag())

  def test_flag(self):
    self.obj.color_resolution      = 1
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 0
    self.assertEqual(int("00000000", 2), self.obj.flag())

    self.obj.color_resolution      = 1
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 1
    self.assertEqual(int("10000000", 2), self.obj.flag())

    self.obj.color_resolution      = 8
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 1
    self.assertEqual(int("11110000", 2), self.obj.flag())

    self.obj.color_resolution      = 8
    self.obj.is_sorted_color_table = True
    self.obj.color_table_size      = 1
    self.assertEqual(int("11111000", 2), self.obj.flag())

    self.obj.color_resolution      = 8
    self.obj.is_sorted_color_table = True
    self.obj.color_table_size      = 8
    self.assertEqual(int("11111111", 2), self.obj.flag())

  def test_write(self):
    sio = StringIO.StringIO()
    self.obj.width                  = 0x1234
    self.obj.height                 = 0x5678
    self.obj.color_resolution       = 8
    self.obj.is_sorted_color_table  = False
    self.obj.color_table_size       = 0
    self.obj.background_color_index = 0x90
    self.obj.pixel_aspect_ratio     = 0xAB
    self.obj.write(sio)

    self.assertEqual(
      "GIF87a\x34\x12\x78\x56\x70\x90\xAB",
      sio.getvalue())


class TestImageBlockHeader(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.ImageBlockHeader()

  def test_init(self):
    self.assertEqual(0,     self.obj.left)
    self.assertEqual(0,     self.obj.top)
    self.assertEqual(0,     self.obj.width)
    self.assertEqual(0,     self.obj.height)
    self.assertEqual(False, self.obj.is_interlaced)
    self.assertEqual(False, self.obj.is_sorted_color_table)
    self.assertEqual(0,     self.obj.color_table_size)

  def test_has_color_table_flag(self):
    self.obj.color_table_size = 0
    self.assertEqual(0, self.obj.has_color_table_flag())
    self.obj.color_table_size = 1
    self.assertEqual(1, self.obj.has_color_table_flag())
    self.obj.color_table_size = 8
    self.assertEqual(1, self.obj.has_color_table_flag())

  def test_is_interlaced_flag(self):
    self.obj.is_interlaced = False
    self.assertEqual(0, self.obj.is_interlaced_flag())
    self.obj.is_interlaced = True
    self.assertEqual(1, self.obj.is_interlaced_flag())

  def test_is_sorted_color_table_flag(self):
    self.obj.is_sorted_color_table = False
    self.assertEqual(0, self.obj.is_sorted_color_table_flag())
    self.obj.is_sorted_color_table = True
    self.assertEqual(1, self.obj.is_sorted_color_table_flag())

  def test_color_table_size_flag(self):
    self.obj.color_table_size = 0
    self.assertEqual(0, self.obj.color_table_size_flag())
    self.obj.color_table_size = 1
    self.assertEqual(0, self.obj.color_table_size_flag())
    self.obj.color_table_size = 8
    self.assertEqual(7, self.obj.color_table_size_flag())

  def test_flag(self):
    self.obj.is_interlaced         = False
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 0
    self.assertEqual(int("00000000", 2), self.obj.flag())

    self.obj.is_interlaced         = False
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 1
    self.assertEqual(int("10000000", 2), self.obj.flag())

    self.obj.is_interlaced         = True
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 1
    self.assertEqual(int("11000000", 2), self.obj.flag())

    self.obj.is_interlaced         = True
    self.obj.is_sorted_color_table = True
    self.obj.color_table_size      = 1
    self.assertEqual(int("11100000", 2), self.obj.flag())

    self.obj.is_interlaced         = True
    self.obj.is_sorted_color_table = True
    self.obj.color_table_size      = 8
    self.assertEqual(int("11100111", 2), self.obj.flag())

  def test_write(self):
    sio = StringIO.StringIO()
    self.obj.left                  = 0x1234
    self.obj.top                   = 0x5678
    self.obj.width                 = 0x9ABC
    self.obj.height                = 0xDEF0
    self.obj.is_interlaced         = False
    self.obj.is_sorted_color_table = False
    self.obj.color_table_size      = 8
    self.obj.write(sio)

    self.assertEqual(
      "\x2C\x34\x12\x78\x56\xBC\x9A\xF0\xDE\x87",
      sio.getvalue())


class TestTrailer(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.Trailer()

  def test_init(self):
    pass

  def test_write(self):
    sio = StringIO.StringIO()
    self.obj.write(sio)

    self.assertEqual(
      "\x3B",
      sio.getvalue())


class TestColorTable(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.ColorTable()

  def test_init(self):
    self.assertEqual([], self.obj.table)

  def test_size(self):
    self.assertEqual(0, self.obj.size())

  def test_bit_size(self):
    self.assertEqual(8, self.obj.bit_size())

  def test_append(self):
    self.assertEqual(0, self.obj.size())

    self.obj.append((1, 2, 3))
    self.assertEqual(1, self.obj.size())
    self.assertEqual((1, 2, 3), self.obj.table[-1])

    self.obj.append((4, 5, 6))
    self.assertEqual(2, self.obj.size())
    self.assertEqual((4, 5, 6), self.obj.table[-1])

  def test_write__empty(self):
    sio = StringIO.StringIO()
    self.obj.write(sio)

    expected = "".join(["\x00\x00\x00" for i in range(256)])
    self.assertEqual(expected, sio.getvalue())

  def test_write__one(self):
    sio = StringIO.StringIO()
    self.obj.append((0xFD, 0xFE, 0xFF))
    self.obj.write(sio)

    expected  = "\xFD\xFE\xFF"
    expected += "".join(["\x00\x00\x00" for i in range(255)])
    self.assertEqual(expected, sio.getvalue())

  def test_write__full(self):
    sio = StringIO.StringIO()
    for i in range(256):
      self.obj.append((0xFF, 0xFF, 0xFF))
    self.obj.write(sio)

    expected = "".join(["\xFF\xFF\xFF" for i in range(256)])
    self.assertEqual(expected, sio.getvalue())


if __name__ == "__main__":
  unittest.main()
