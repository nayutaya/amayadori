# -*- coding: utf-8 -*-

import unittest
import datetime

import jmalib


class TestTimeUtility(unittest.TestCase):
  def setUp(self):
    self.klass = jmalib.TimeUtility

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
