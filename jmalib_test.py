# -*- coding: utf-8 -*-

import unittest
import datetime

import jmalib
import imglib


class TestJmaLib(unittest.TestCase):
  def setUp(self):
    pass

  def test_parse_radar_js(self):
    src = """
      var idx=0;
      ImgRadar1kmColor[idx++] = new ImageInfo("200908061355-00.png","");
      ImgRadar1kmColor[idx++] = new ImageInfo("200908061350-00.png","");
      ImgRadar1kmColor[idx++] = new ImageInfo("200908061345-00.png","");
      ImgRadar1kmColor[idx++] = new ImageInfo("200908061340-00.png","");
      ImgRadar1kmColor[idx++] = new ImageInfo("200908061335-00.png","");
      """
    expected = [
      (datetime.datetime(2009, 8, 6, 13, 55), 0),
      (datetime.datetime(2009, 8, 6, 13, 50), 0),
      (datetime.datetime(2009, 8, 6, 13, 45), 0),
      (datetime.datetime(2009, 8, 6, 13, 40), 0),
      (datetime.datetime(2009, 8, 6, 13, 35), 0),
    ]
    self.assertEqual(
      expected,
      jmalib.parse_radar_js(src))

  def test_parse_nowcast_js(self):
    src = """
      var idx=0;
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-06.png","");
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-05.png","");
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-04.png","");
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-03.png","");
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-02.png","");
      ImgNowcastColor[idx++] = new ImageInfo("200908061400-01.png","");
      """
    expected = [
      (datetime.datetime(2009, 8, 6, 14, 0), 6),
      (datetime.datetime(2009, 8, 6, 14, 0), 5),
      (datetime.datetime(2009, 8, 6, 14, 0), 4),
      (datetime.datetime(2009, 8, 6, 14, 0), 3),
      (datetime.datetime(2009, 8, 6, 14, 0), 2),
      (datetime.datetime(2009, 8, 6, 14, 0), 1),
    ]
    self.assertEqual(
      expected,
      jmalib.parse_nowcast_js(src))

  def test_get_latest_time(self):
    time_and_ordinals = [
      (datetime.datetime(2009, 8, 6, 13, 55), 0),
      (datetime.datetime(2009, 8, 6, 13, 50), 1),
      (datetime.datetime(2009, 8, 6, 13, 45), 2),
      (datetime.datetime(2009, 8, 6, 13, 40), 3),
      (datetime.datetime(2009, 8, 6, 13, 35), 4),
    ]
    self.assertEqual(
      datetime.datetime(2009, 8, 6, 13, 55),
      jmalib.get_latest_time(time_and_ordinals))

  def test_get_current_radar_time(self):
    def fetcher(url):
      src = """
        var idx=0;
        ImgRadar1kmColor[idx++] = new ImageInfo("200908061355-00.png","");
        ImgRadar1kmColor[idx++] = new ImageInfo("200908061350-00.png","");
        """
      return src
    self.assertEqual(
      datetime.datetime(2009, 8, 6, 13, 55),
      jmalib.get_current_radar_time(fetcher))

  def test_get_current_nowcast_time(self):
    def fetcher(url):
      src = """
        var idx=0;
        ImgNowcastColor[idx++] = new ImageInfo("200908061355-06.png","");
        ImgNowcastColor[idx++] = new ImageInfo("200908061350-05.png","");
        """
      return src
    self.assertEqual(
      datetime.datetime(2009, 8, 6, 13, 55),
      jmalib.get_current_nowcast_time(fetcher))

  def test_create_radar_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/000/200001010000-00.png",
      jmalib.create_radar_image_url(0, datetime.datetime(2000, 1, 1, 0, 0)))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/999/199912312359-00.png",
      jmalib.create_radar_image_url(999, datetime.datetime(1999, 12, 31, 23, 59)))

  def test_create_nowcast_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/000/200001010000-00.png",
      jmalib.create_nowcast_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 0))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/999/199912312359-99.png",
      jmalib.create_nowcast_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99))

  def test_create_image_url(self):
    self.assertEqual(
      jmalib.create_radar_image_url(0, datetime.datetime(2000, 1, 1, 0, 0)),
      jmalib.create_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 0))
    self.assertEqual(
      jmalib.create_radar_image_url(999, datetime.datetime(1999, 12, 31, 23, 59)),
      jmalib.create_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 0))
    self.assertEqual(
      jmalib.create_nowcast_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 1),
      jmalib.create_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 1))
    self.assertEqual(
      jmalib.create_nowcast_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99),
      jmalib.create_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99))

  def test_get_image(self):
    def fetcher(url):
      return "binary"
    self.assertEqual(
      "binary",
      jmalib.get_image(0, datetime.datetime(2000, 1, 1, 0, 0), 0, fetcher))
    self.assertEqual(
      "binary",
      jmalib.get_image(0, datetime.datetime(2000, 1, 1, 0, 0), 1, fetcher))

  def test_is_water_color(self):
    def h(int):
      return imglib.Color.int_to_rgb(int)

    self.assertEqual(True,  jmalib.is_water_color(h(0xC0C0C0)))
    self.assertEqual(True,  jmalib.is_water_color(h(0xC1C1C1)))

    self.assertEqual(True , jmalib.is_water_color(h(0x000000)))
    self.assertEqual(False, jmalib.is_water_color(h(0x000100)))

    list = [
      0x5B719B, 0x5B7298, 0x5C739F, 0x5D739F, 0x5E759E,
      0x5F7597, 0x638099, 0x648191, 0x667D91, 0x687F8F,
      0x6982B8, 0x6E85BC, 0x6F8EA9, 0x708AA2, 0x708EAA,
      0x728D9F, 0x728DA3, 0x728EA9, 0x738DB7, 0x738DC2,
      0x7393B7, 0x748DC0, 0x748FA9, 0x748FAD, 0x758DC9,
      0x7692AF, 0x7A9FA5, 0x7B94C6, 0x7D9DC2, 0x7D9EC1,
      0x7E97C7, 0x7E9CBB, 0x7F9EC0, 0x7F9EC2, 0x809CBE,
      0x809EAC, 0x809EC0, 0x86A4CD, 0x86A6D1, 0x88A6CF,
      0x89A7D1, 0x89AAD3, 0x8AA6D2, 0x8AA7D0, 0x8AA9D2,
      0x8BABD1, 0x8DACD2, 0x8EAAD3, 0x8EADB4, 0x8FADD2,
      0x90ADD3, 0x90AFB7, 0x91AED2, 0x91B0D2, 0x9AB6BA,
      0xB8B8E4, 0xD9D9D9,
    ]
    for int in list:
      self.assertEqual(
        (h(int), True),
        (h(int), jmalib.is_water_color(h(int))))

  def test_is_ground_color(self):
    def h(int):
      return imglib.Color.int_to_rgb(int)

    self.assertEqual(False, jmalib.is_ground_color(h(0x000000)))
    self.assertEqual(True,  jmalib.is_ground_color(h(0x000100)))

    list = [
      0x698B5A, 0x6D8D5E, 0x6D8E5F, 0x6F9060, 0x6F915F,
      0x729562, 0x747B72, 0x749665, 0x759666, 0x759964,
      0x769866, 0x769867, 0x769966, 0x779967, 0x779968,
      0x789584, 0x789585, 0x789B67, 0x799283, 0x7A9D6B,
      0x7A9E6A, 0x7B9B88, 0x7D9E8E, 0x7DA06C, 0x7DA16C,
      0x7DA16D, 0x7E9787, 0x7E9E92, 0x7EA16D, 0x7FA26E,
      0x7FA36F, 0x809F8D, 0x80A07E, 0x80A36F, 0x819C85,
      0x819E92, 0x81A570, 0x82A37F, 0x82A571, 0x82A671,
      0x839F84, 0x83A772, 0x84958A, 0x84A39B, 0x84A773,
      0x84A873, 0x85A874, 0x86A975, 0x86A976, 0x87A977,
      0x87AA76, 0x87AA77, 0x87AB77, 0x88A89B, 0x88AB78,
      0x89A99E, 0x89AAA8, 0x89AB79, 0x89AD79, 0x8AA486,
      0x8AAC79, 0x8AAC7A, 0x8BAB7B, 0x8BAC7B, 0x8BAD7A,
      0x8BAE7B, 0x8CABA7, 0x8CAD7C, 0x8CAE7D, 0x8CAF7C,
      0x8DA7A2, 0x8DAAA6, 0x8DACA7, 0x8DAE7D, 0x8DAE7E,
      0x8DAFAC, 0x8DB07C, 0x8EAF7F, 0x8EB07F, 0x8FAB88,
      0x8FB080, 0x8FB27F, 0x90AC89, 0x90B080, 0x90B081,
      0x91B182, 0x92AE8F, 0x92B283, 0x92B481, 0x93B283,
      0x93B284, 0x93B484, 0x94B29A, 0x94B29C, 0x95B486,
      0x96B588, 0x97B588, 0x97B688, 0x98B889, 0x99B78A,
      0x99B78B, 0x99B7A5, 0x9AB88B, 0x9BB98D, 0x9CB98E,
      0x9DB9AB, 0x9DBA8F, 0x9EBA90, 0x9EBB90, 0x9FBB91,
      0xA0BC93, 0xA1BD93, 0xA1BD94, 0xA1BD95, 0xA2BD94,
      0xA2BE95, 0xA2BE96, 0xA3BF97, 0xA4BF97, 0xA5C097,
    ]
    for int in list:
      self.assertEqual(
        (h(int), True),
        (h(int), jmalib.is_ground_color(h(int))))

  def test_color_reduction(self):
    target = jmalib.color_reduction

    # ïsñæ
    #self.assertEqual((192,   0, 192), target((  0,   0,   0)))

    # âJâ_
    self.assertEqual((255,   0,   0), target((255,   0,   0)))
    self.assertEqual((255,   0, 255), target((255,   0, 255)))
    self.assertEqual((255, 153,   0), target((255, 153,   0)))
    self.assertEqual((255, 255,   0), target((255, 255,   0)))
    self.assertEqual((  0, 255,   0), target((  0, 255,   0)))
    self.assertEqual((  0,   0, 255), target((  0,   0, 255)))
    self.assertEqual(( 51, 102, 255), target(( 51, 102, 255)))
    self.assertEqual((153, 204, 255), target((153, 204, 255)))

    # äœë™ì_
    self.assertEqual(( 96, 128,  96), target(( 96,  57,  19)))

    # ìsìπï{åßã´äE
    self.assertEqual((255, 255, 255), target((230, 230, 230)))

    # äCä›ã´äE/ÉOÉäÉbÉh
    self.assertEqual((102, 102, 102), target((102, 102, 102)))

    # äCä›ã´äE
    self.assertEqual((255, 255, 255), target((255, 255, 255)))
    self.assertEqual((116, 123, 114), target((116, 123, 114)))
    self.assertEqual((160, 160, 160), target((160, 160, 160)))

    # ínï\
    self.assertEqual(( 96, 128,  96), target((  0,   1,   0)))

    # êÖñ 
    self.assertEqual(( 64,  96, 128), target((  0,   0,   1)))

  def test_get_minimum_rainfall_from_rgb(self):
    target = jmalib.get_minimum_rainfall_from_rgb

    self.assertEqual(None, target((  0,   0,   0)))

    self.assertEqual( 0, target((153, 204, 255)))
    self.assertEqual( 1, target(( 51, 102, 255)))
    self.assertEqual( 5, target((  0,   0, 255)))
    self.assertEqual(10, target((  0, 255,   0)))
    self.assertEqual(20, target((255, 255,   0)))
    self.assertEqual(30, target((255, 153,   0)))
    self.assertEqual(50, target((255,   0, 255)))
    self.assertEqual(80, target((255,   0,   0)))

  def test_get_maximum_rainfall_from_rgb(self):
    target = jmalib.get_maximum_rainfall_from_rgb

    self.assertEqual(None, target((  0,   0,   0)))

    self.assertEqual(  1, target((153, 204, 255)))
    self.assertEqual(  5, target(( 51, 102, 255)))
    self.assertEqual( 10, target((  0,   0, 255)))
    self.assertEqual( 20, target((  0, 255,   0)))
    self.assertEqual( 30, target((255, 255,   0)))
    self.assertEqual( 50, target((255, 153,   0)))
    self.assertEqual( 80, target((255,   0, 255)))
    self.assertEqual(100, target((255,   0,   0)))

  def test_get_rainfall_from_bitmap(self):
    target = jmalib.get_rainfall_from_bitmap

    bitmap = imglib.RgbBitmap(1, 1)
    bitmap.set_pixels([(0, 0, 0)])
    self.assertEqual((0, 0), target(bitmap))

    bitmap = imglib.RgbBitmap(3, 1)
    bitmap.set_pixels([
      (  0,   0,   0),
      (153, 204, 255),
      (255,   0,   0),
    ])
    self.assertEqual((0, 100), target(bitmap))

    bitmap = imglib.RgbBitmap(1, 3)
    bitmap.set_pixels([
      (  0,   0,   0),
      ( 51, 102, 255),
      (255,   0, 255),
    ])
    self.assertEqual((1, 80), target(bitmap))


if __name__ == "__main__":
  unittest.main()
