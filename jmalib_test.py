# -*- coding: utf-8 -*-

import unittest
import datetime

import jmalib
import imglib


class TestRadarNowCast(unittest.TestCase):
  def setUp(self):
    self.klass = jmalib.RadarNowCast

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
      self.klass.parse_radar_js(src))

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
      self.klass.parse_nowcast_js(src))

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
      self.klass.get_latest_time(time_and_ordinals))

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
      self.klass.get_current_radar_time(fetcher))

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
      self.klass.get_current_nowcast_time(fetcher))

  def test_create_radar_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/000/200001010000-00.png",
      self.klass.create_radar_image_url(0, datetime.datetime(2000, 1, 1, 0, 0)))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/999/199912312359-00.png",
      self.klass.create_radar_image_url(999, datetime.datetime(1999, 12, 31, 23, 59)))

  def test_create_nowcast_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/000/200001010000-00.png",
      self.klass.create_nowcast_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 0))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/999/199912312359-99.png",
      self.klass.create_nowcast_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99))

  def test_create_image_url(self):
    self.assertEqual(
      self.klass.create_radar_image_url(0, datetime.datetime(2000, 1, 1, 0, 0)),
      self.klass.create_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 0))
    self.assertEqual(
      self.klass.create_radar_image_url(999, datetime.datetime(1999, 12, 31, 23, 59)),
      self.klass.create_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 0))
    self.assertEqual(
      self.klass.create_nowcast_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 1),
      self.klass.create_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 1))
    self.assertEqual(
      self.klass.create_nowcast_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99),
      self.klass.create_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99))

  def test_get_image(self):
    def fetcher(url):
      return "binary"
    self.assertEqual(
      "binary",
      self.klass.get_image(0, datetime.datetime(2000, 1, 1, 0, 0), 0, fetcher))
    self.assertEqual(
      "binary",
      self.klass.get_image(0, datetime.datetime(2000, 1, 1, 0, 0), 1, fetcher))

  def test_is_water_color(self):
    def h(int):
      return imglib.Color.int_to_rgb(int)

    self.assertEqual(False, self.klass.is_water_color(h(0x000100)))
    self.assertEqual(True,  self.klass.is_water_color(h(0xC0C0C0)))
    self.assertEqual(True,  self.klass.is_water_color(h(0xC1C1C1)))

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
        (h(int), self.klass.is_water_color(h(int))))


if __name__ == "__main__":
  unittest.main()
