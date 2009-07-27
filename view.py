# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import area

class ViewPage(webapp.RequestHandler):
  def get(self, lat, lng):
    lnglat = (float(lng), float(lat))
    nearest_area = area.AreaManager.get_nearest_area(lnglat)
    if nearest_area == None:
      self.error("範囲外です。")

    html = str(nearest_area.code)

    self.response.headers["Content-Type"] = "text/plain"
    self.response.out.write(html)

  def error(self, message):
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
