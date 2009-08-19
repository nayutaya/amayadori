# -*- coding: utf-8 -*-

import re


def dms_to_deg(dms):
  regexp = re.compile(r"^([\+\-])?(\d+)\.(\d+)\.(\d+\.\d+)$")
  match  = regexp.match(dms)
  sign   = (1 if match.group(1) != "-" else -1)
  deg    = float(match.group(2))
  min    = float(match.group(3))
  sec    = float(match.group(4))
  return sign * (deg + (min / 60) + (sec / 3600))
