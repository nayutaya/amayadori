# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import area

class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    lnglat = (float(lng), float(lat))
    nearest_area = area.AreaManager.get_nearest_area(lnglat)
    if nearest_area == None:
      self.error_message("範囲外です。")

    xy = nearest_area.lnglat_to_xy(lnglat)

    values = {
      "area_code": str(nearest_area.code),
      "lat": str(lnglat[1]),
      "lng": str(lnglat[0]),
      "x": str(xy[0]),
      "y": str(xy[1]),
    }

    path = os.path.join(os.path.dirname(__file__), "view.html")
    html = template.render(path, values)

    self.response.out.write(html)

  def error_message(self, message):
    html = """<html><head>"""
    html += """<meta http-equiv="content-type" content="text/html; charset=utf-8">"""
    html += """<title></title>"""
    html += """</head><body>"""
    html += "<div>" + message + "</div>"
    html += """</body></html>"""

    self.response.headers["Content-Type"] = "text/html"
    self.response.out.write(html)


application = webapp.WSGIApplication(
  [(r"/view/([\+\-]?\d+(?:\.\d+)?)/([\+\-]?\d+(?:\.\d+)?)", ViewPage)],
  debug = True)


if __name__ == "__main__":
  run_wsgi_app(application)
