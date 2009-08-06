# -*- coding: utf-8 -*-

import unittest
import datetime

import jmalib


class TestTimeUtility(unittest.TestCase):
  def setUp(self):
    self.klass = jmalib.TimeUtility

  def test_get_jst_now(self):
    self.assertEqual(
      datetime.datetime(2000, 1, 1, 9, 0),
      self.klass.get_jst_now(datetime.datetime(2000, 1, 1, 0, 0)))

  def test_get_per_minute_time(self):
    self.assertEqual(
      datetime.datetime(2000, 1, 1, 0, 0),
      self.klass.get_per_minute_time(datetime.datetime(2000, 1, 1, 0, 0, 0)))
    self.assertEqual(
      datetime.datetime(1999, 12, 31, 23, 59),
      self.klass.get_per_minute_time(datetime.datetime(1999, 12, 31, 23, 59, 59)))


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

if __name__ == "__main__":
  unittest.main()
