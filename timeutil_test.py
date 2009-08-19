# -*- coding: utf-8 -*-

import unittest
import datetime

import timeutil


class TestTimeUtility(unittest.TestCase):
  def setUp(self):
    pass

  def test_get_jst_now(self):
    self.assertEqual(
      datetime.datetime(2000, 1, 1, 9, 0),
      timeutil.get_jst_now(datetime.datetime(2000, 1, 1, 0, 0)))

  def test_get_per_minute_time(self):
    self.assertEqual(
      datetime.datetime(2000, 1, 1, 0, 0),
      timeutil.get_per_minute_time(datetime.datetime(2000, 1, 1, 0, 0, 0)))
    self.assertEqual(
      datetime.datetime(1999, 12, 31, 23, 59),
      timeutil.get_per_minute_time(datetime.datetime(1999, 12, 31, 23, 59, 59)))

  def test_timedelta_to_second(self):
    target = timeutil.timedelta_to_second

    self.assertEqual(0, target(datetime.timedelta(days = 0)))
    self.assertEqual(0, target(datetime.timedelta(seconds = 0)))

    self.assertEqual( 60 * 60 * 24, target(datetime.timedelta(days =  1)))
    self.assertEqual(-60 * 60 * 24, target(datetime.timedelta(days = -1)))

    self.assertEqual( 1, target(datetime.timedelta(seconds =  1)))
    self.assertEqual(-1, target(datetime.timedelta(seconds = -1)))

  def test_timedelta_to_word(self):
    target = timeutil.timedelta_to_word

    self.assertEqual("0分前", target(datetime.timedelta(seconds = 0)))
    self.assertEqual("0分前", target(datetime.timedelta(seconds = -59)))
    self.assertEqual("1分前", target(datetime.timedelta(seconds = -60)))
    self.assertEqual("2分前", target(datetime.timedelta(seconds = -120)))

    self.assertEqual("0分後", target(datetime.timedelta(seconds = 1)))
    self.assertEqual("0分後", target(datetime.timedelta(seconds = 59)))
    self.assertEqual("1分後", target(datetime.timedelta(seconds = 60)))
    self.assertEqual("2分後", target(datetime.timedelta(seconds = 120)))

if __name__ == "__main__":
  unittest.main()
