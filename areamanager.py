# -*- coding: utf-8 -*-

class AreaInfo:
  def __init__(self, name, code, dxy, gxy1, gxy2, glnglat1, glnglat2):
    self.name     = name     # 名称
    self.code     = code     # エリアコード
    self.dxy      = dxy      # 画像サイズ (px)
    self.gxy1     = gxy1     # 左上グリッド座標 (px)
    self.gxy2     = gxy2     # 右下グリッド座標 (px)
    self.glnglat1 = glnglat1 # 左上グリッド座標 (deg)
    self.glnglat2 = glnglat2 # 右下グリッド座標 (deg)

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

  def north(self): return self.glat1() + (self.gy1()               * float(self.gdlat()) / self.gdy())
  def south(self): return self.glat2() - ((self.dy() - self.gy2()) * float(self.gdlat()) / self.gdy())
  def west(self):  return self.glng1() - (self.gx1()               * float(self.gdlng()) / self.gdx())
  def east(self):  return self.glng2() + ((self.dx() - self.gx2()) * float(self.gdlng()) / self.gdx())

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

  def include_lnglat(self, lnglat):
    return self.include_xy(self.lnglat_to_xy(lnglat))


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

  @classmethod
  def get_nearest_area(cls, lnglat):
    all_areas        = cls.areas
    available_areas  = cls.get_available_areas_from(all_areas, lnglat)
    area_distances   = cls.get_distances_from(available_areas, lnglat)
    sorted_distances = cls.sort_by_distance(area_distances)
    if len(sorted_distances) > 0:
      return sorted_distances[0][0]
    else:
      return None

  @staticmethod
  def get_available_areas_from(areas, lnglat):
    return [area for area in areas if area.include_lnglat(lnglat)]

  @staticmethod
  def get_distances_from(areas, lnglat):
    return [(area, area.distance_from_center(lnglat)) for area in areas]

  @staticmethod
  def sort_by_distance(distances):
    def compare(a, b):
      (area1, distance1) = a
      (area2, distance2) = b
      return distance1 - distance2
    a = [x for x in distances]
    a.sort(compare)
    return a

#                             name                   code dxy         gxy1        gxy2        glnglat1    glnglat2
AreaManager.register(AreaInfo(u"北海道地方(北西部)", 201, (550, 455), ( 32,  97), (474, 400), (139,  45), (145,  42)))
AreaManager.register(AreaInfo(u"北海道地方(東部)",   202, (550, 455), ( 13,  75), (457, 379), (141,  45), (147,  42)))
AreaManager.register(AreaInfo(u"北海道地方(南西部)", 203, (550, 455), ( 29,  84), (480, 387), (138,  44), (144,  41)))
AreaManager.register(AreaInfo(u"東北地方(北部)",     204, (550, 455), ( 40,  17), (509, 421), (138,  42), (144,  38)))
AreaManager.register(AreaInfo(u"東北地方(南部)",     205, (550, 455), ( 75,  25), (476, 430), (138,  40), (143,  36)))
AreaManager.register(AreaInfo(u"関東地方",           206, (550, 455), ( 28,  58), (527, 362), (137,  37), (143,  34)))
AreaManager.register(AreaInfo(u"甲信地方",           207, (550, 455), ( 29,   8), (524, 412), (136,  38), (142,  34)))
AreaManager.register(AreaInfo(u"北陸地方(東部)",     208, (550, 455), ( 27,  84), (511, 388), (136,  39), (142,  36)))
AreaManager.register(AreaInfo(u"北陸地方(西部)",     209, (550, 455), ( 17,  58), (510, 362), (134,  38), (140,  35)))
AreaManager.register(AreaInfo(u"東海地方",           210, (550, 455), ( 74,  84), (494, 387), (136,  36), (141,  33)))
AreaManager.register(AreaInfo(u"近畿地方",           211, (550, 455), ( 54,  93), (473, 396), (133,  36), (138,  33)))
AreaManager.register(AreaInfo(u"中国地方",           212, (550, 455), ( 26,   8), (529, 413), (130,  37), (136,  33)))
AreaManager.register(AreaInfo(u"四国地方",           213, (550, 455), ( 45, 101), (469, 404), (131,  35), (136,  32)))
AreaManager.register(AreaInfo(u"九州地方(北部)",     214, (550, 455), ( 51,  67), (477, 371), (128,  35), (133,  32)))
AreaManager.register(AreaInfo(u"九州地方(南部)",     215, (550, 455), ( 91,  50), (527, 354), (129,  33), (134,  30)))
AreaManager.register(AreaInfo(u"奄美地方",           216, (550, 455), ( 12,  67), (459, 370), (127,  30), (132,  27)))
AreaManager.register(AreaInfo(u"沖縄本島地方",       217, (550, 455), ( 53,  50), (511, 354), (126,  28), (131,  25)))
AreaManager.register(AreaInfo(u"大東島地方",         218, (550, 455), (  8,  33), (465, 337), (127,  28), (132,  25)))
AreaManager.register(AreaInfo(u"宮古・八重山地方",   219, (550, 455), ( 35,  84), (499, 387), (122,  26), (127,  23)))


def dump_kml():
  print """<?xml version="1.0" encoding="UTF-8"?>"""
  print """<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">"""
  print "<Folder>"

  for area in AreaManager.areas:
    if area.glng1() > 0:
      print "<GroundOverlay>"
      print "<name>" + str(area.code) + "</name>"
      print "<color>bdffffff</color>"
      print "<Icon>"
      print "<href>http://amayadori-opt.appspot.com/images/" + str(area.code) + "/observed.png</href>"
      print "</Icon>"
      print "<LatLonBox>"
      print "<north>" + str(area.north()) + "</north>"
      print "<south>" + str(area.south()) + "</south>"
      print "<east>" + str(area.east()) + "</east>"
      print "<west>" + str(area.west()) + "</west>"
      print "</LatLonBox>"
      print "</GroundOverlay>"

  print "</Folder>"
  print """</kml>"""


if __name__ == "__main__":
  #dump_kml()
  lnglat = (135.0, 35.0)
  area = AreaManager.get_nearest_area(lnglat)
  print area
