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


class TestUncompressedImageBlockData(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.UncompressedImageBlockData()

  def test_init(self):
    self.assertEqual([], self.obj.pixels)

  def test_size(self):
    self.assertEqual(0, self.obj.size())

  def test_append(self):
    self.assertEqual(0, self.obj.size())

    self.obj.append(0)
    self.assertEqual(1, self.obj.size())
    self.assertEqual(0, self.obj.pixels[-1])

    self.obj.append(1)
    self.assertEqual(2, self.obj.size())
    self.assertEqual(1, self.obj.pixels[-1])

  def test_bitsets__empty(self):
    expected = [
      "100000000", # clear code
      "100000001", # end code
    ]
    self.assertEqual(expected, self.obj.bitsets())

  def test_bitsets__4pixel(self):
    self.obj.append(int("11111111", 2))
    self.obj.append(int("11110000", 2))
    self.obj.append(int("11001100", 2))
    self.obj.append(int("10101010", 2))

    expected = [
      "100000000", # clear code
      "011111111",
      "011110000",
      "011001100",
      "010101010",
      "100000001", # end code
    ]
    self.assertEqual(expected, self.obj.bitsets())

  def test_bitsets__254pixel(self):
    for i in range(254):
      self.obj.append(0)

    expected = []
    expected.append("100000000") # clear code
    for i in range(254):
      expected.append("000000000")
    expected.append("100000001") # end code
    self.assertEqual(expected, self.obj.bitsets())

  def test_bitsets__255pixel(self):
    for i in range(255):
      self.obj.append(0)

    expected = []
    expected.append("100000000") # clear code
    for i in range(254):
      expected.append("000000000")
    expected.append("100000000") # clear code
    expected.append("000000000")
    expected.append("100000001") # end code
    self.assertEqual(expected, self.obj.bitsets())

  def test_bitsets__509pixel(self):
    for i in range(509):
      self.obj.append(0)

    expected = []
    expected.append("100000000") # clear code
    for i in range(254):
      expected.append("000000000")
    expected.append("100000000") # clear code
    for i in range(254):
      expected.append("000000000")
    expected.append("100000000") # clear code
    expected.append("000000000")
    expected.append("100000001") # end code
    self.assertEqual(expected, self.obj.bitsets())


  def test_bits_to_bytes__empty(self):
    self.assertEqual(
      [],
      self.obj.bits_to_bytes(""))

  def test_bits_to_bytes__1byte(self):
    self.assertEqual(
      [int("11111111", 2)],
      self.obj.bits_to_bytes("11111111"))

  def test_bits_to_bytes__less_than_1byte(self):
    self.assertEqual(
      [int("000000001", 2)],
      self.obj.bits_to_bytes("1"))
    self.assertEqual(
      [int("00001111", 2)],
      self.obj.bits_to_bytes("1111"))
    self.assertEqual(
      [int("01111111", 2)],
      self.obj.bits_to_bytes("1111111"))

  def test_bits_to_bytes__1byte_and_half(self):
    self.assertEqual(
      [int("10000000", 2), int("1111", 2)],
      self.obj.bits_to_bytes("100000001111"))

  def test_bytes__empty(self):
    expected = [
      int("00000000", 2),
      int("00000011", 2),
      int("00000010", 2),
    ]
    self.assertEqual(expected, self.obj.bytes())

  def test_bytes__4pixel(self):
    self.obj.append(int("11111111", 2))
    self.obj.append(int("11110000", 2))
    self.obj.append(int("11001100", 2))
    self.obj.append(int("10101010", 2))

    expected = [
      int("00000000", 2),
      int("11111111", 2),
      int("11000001", 2),
      int("01100011", 2),
      int("10100110", 2),
      int("00101010", 2),
      int("00100000", 2),
    ]
    self.assertEqual(expected, self.obj.bytes())


class TestImageBlock(unittest.TestCase):
  def setUp(self):
    self.obj = gifrawlib.ImageBlock()

  def test_init(self):
    self.assertEqual(8,  self.obj.minimum_code)
    self.assertEqual([], self.obj.data)

  def test_write__empty(self):
    sio = StringIO.StringIO()
    self.obj.minimum_code = 8
    self.obj.data         = []
    self.obj.write(sio)

    self.assertEqual(
      "\x08\x00",
      sio.getvalue())

  def test_write__1byte(self):
    sio = StringIO.StringIO()
    self.obj.minimum_code = 8
    self.obj.data         = [0xFF]
    self.obj.write(sio)

    self.assertEqual(
      "\x08\x01\xFF\x00",
      sio.getvalue())

  def test_write__256byte(self):
    sio = StringIO.StringIO()
    self.obj.minimum_code = 8
    self.obj.data         = [0xCC for i in range(256)]
    self.obj.write(sio)

    expected  = "\x08"
    expected += "\xFF" + "".join(["\xCC" for i in range(255)])
    expected += "\x01" + "\xCC"
    expected += "\x00"
    self.assertEqual(expected, sio.getvalue())

  def test_write__511byte(self):
    sio = StringIO.StringIO()
    self.obj.minimum_code = 8
    self.obj.data         = [0xCC for i in range(511)]
    self.obj.write(sio)

    expected  = "\x08"
    expected += "\xFF" + "".join(["\xCC" for i in range(255)])
    expected += "\xFF" + "".join(["\xCC" for i in range(255)])
    expected += "\x01" + "\xCC"
    expected += "\x00"
    self.assertEqual(expected, sio.getvalue())


if __name__ == "__main__":
  unittest.main()
