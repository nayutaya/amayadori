# -*- coding: utf-8 -*-

class AreaInfo:
  def __init__(self, name, code, dxy, gxy1, gxy2, glnglat1, glnglat2):
    self.name     = name
    self.code     = code
    self.dxy      = dxy  # px
    self.gxy1     = gxy1 # px
    self.gxy2     = gxy2 # px
    self.glnglat1 = glnglat1 # deg
    self.glnglat2 = glnglat2 # deg

  def dx(self): return self.dxy[0]
  def dy(self): return self.dxy[1]
  def cx(self): return int(self.dx() / 2.0)
  def cy(self): return int(self.dy() / 2.0)

  def gx1(self): return self.gxy1[0]
  def gy1(self): return self.gxy1[1]
  def gx2(self): return self.gxy2[0]
  def gy2(self): return self.gxy2[1]
  def gdx(self): return self.gx2() - self.gx1()
  def gdy(self): return self.gy2() - self.gy1()

  def glng1(self): return self.glnglat1[0]
  def glat1(self): return self.glnglat1[1]
  def glng2(self): return self.glnglat2[0]
  def glat2(self): return self.glnglat2[1]
  def gdlng(self): return self.glng2() - self.glng1()
  def gdlat(self): return self.glat1() - self.glat2()

  def lng_to_x(self, lng):
    return int((lng - self.glng1()) / (float(+self.gdlng()) / self.gdx()) + self.gx1())

  def lat_to_y(self, lat):
    return int((lat - self.glat2()) / (float(-self.gdlat()) / self.gdy()) + self.gy2())

  def lnglat_to_xy(self, lnglat):
    return (self.lng_to_x(lnglat[0]), self.lat_to_y(lnglat[1]))

  def distance_from_center(self, lnglat):
    xy = self.lnglat_to_xy(lnglat)
    dx = self.cx() - xy[0]
    dy = self.cy() - xy[1]
    return dx * dx + dy * dy

  def include_xy(self, xy):
    x, y = xy
    return (x >= 0) and (y >= 0) and (x < self.dx()) and (y < self.dy())


class AreaManager:
  areas = []
  def __init__(self):
    pass

  @classmethod
  def register(cls, area):
    cls.areas.append(area)

  @classmethod
  def find_by_code(cls, code):
    for area in cls.areas:
      if area.code == code:
        return area
    return None


AreaManager.register(
  AreaInfo(
    name     = "近畿地方",
    code     = 211,
    dxy      = (550, 455),
    gxy1     = ( 54,  93),
    gxy2     = (473, 396),
    glnglat1 = (133,  36),
    glnglat2 = (138,  33)))

#print AreaManager.areas
#print AreaManager.find_by_code(211)

