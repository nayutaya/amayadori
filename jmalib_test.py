# -*- coding: utf-8 -*-

import unittest
import datetime

import jmalib


class TestRadarNowCast(unittest.TestCase):
  def setUp(self):
    pass

  def test_create_observed_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/000/200001010000-00.png",
      jmalib.RadarNowCast.create_observed_image_url(0, datetime.datetime(2000, 1, 1, 0, 0)))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/radar/999/199912312359-00.png",
      jmalib.RadarNowCast.create_observed_image_url(999, datetime.datetime(1999, 12, 31, 23, 59)))

  def test_create_predictive_image_url(self):
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/000/200001010000-00.png",
      jmalib.RadarNowCast.create_predictive_image_url(0, datetime.datetime(2000, 1, 1, 0, 0), 0))
    self.assertEqual(
      "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/999/199912312359-99.png",
      jmalib.RadarNowCast.create_predictive_image_url(999, datetime.datetime(1999, 12, 31, 23, 59), 99))

if __name__ == "__main__":
  unittest.main()
