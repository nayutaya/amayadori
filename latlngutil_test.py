# -*- coding: utf-8 -*-

import unittest

import latlngutil


class TestLatLngUtility(unittest.TestCase):
  def setUp(self):
    pass

  def test_dms_to_deg(self):
    target = latlngutil.dms_to_deg
    self.assertEqual(0.0,  target("0.0.0.0"))
    self.assertEqual(1.0,  target(" 1.0.0.0"))
    self.assertEqual(1.0,  target("+1.0.0.0"))
    self.assertEqual(-1.0, target("-1.0.0.0"))

    self.assertEqual(1.0, target("0.60.0.0"))
    self.assertEqual(1.0, target("0.0.3600.0"))
    self.assertEqual(1.5101, target("1.30.36.36"))

  def test_softbank_pos_to_dms_dms(self):
    target = latlngutil.softbank_pos_to_dms_dms

    self.assertEqual((None, None), target(""))
    self.assertEqual(( "0.0.0.0",  "0.0.0.0"), target("N0.0.0.0E0.0.0.0"))
    self.assertEqual(("-0.0.0.0", "-0.0.0.0"), target("S0.0.0.0W0.0.0.0"))

    self.assertEqual(("12.34.56.78", "0.0.0.0"), target("N12.34.56.78E0.0.0.0"))
    self.assertEqual(("0.0.0.0", "12.34.56.78"), target("N0.0.0.0E12.34.56.78"))


if __name__ == "__main__":
  unittest.main()
