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


if __name__ == "__main__":
  unittest.main()
