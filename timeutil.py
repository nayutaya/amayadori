# -*- coding: utf-8 -*-

import datetime
import re


def yyyymmddhhnn_to_datetime(str):
  regexp = re.compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$")
  match  = regexp.match(str)
  return datetime.datetime(
      int(match.group(1)), int(match.group(2)), int(match.group(3)),
      int(match.group(4)), int(match.group(5)))
