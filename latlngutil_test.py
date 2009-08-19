# -*- coding: utf-8 -*-

import unittest

import latlngutil


class TestLatLngUtility(unittest.TestCase):
  def setUp(self):
    pass

  def test_dms_to_deg(self):
    target = latlngutil.dms_to_deg
    self.assertEqual(0.0,  target("0.0.0.0"))
    self.assertEqual(1.0,  target("+1.0.0.0"))
    self.assertEqual(-1.0, target("-1.0.0.0"))

    self.assertEqual(1.0, target("0.60.0.0"))
    self.assertEqual(1.0, target("0.0.3600.0"))
    self.assertEqual(1.5101, target("1.30.36.36"))


if __name__ == "__main__":
  unittest.main()
