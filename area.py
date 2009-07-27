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


x = -1
#                             name                   code dxy         gxy1        gxy2        glnglat1    glnglat2
AreaManager.register(AreaInfo(u"北海道地方(北西部)", 201, (550, 455), ( 32,  97), (474, 400), (139,  45), (145,  42)))
AreaManager.register(AreaInfo(u"北海道地方(東部)",   202, (550, 455), ( 13,  75), (457, 379), (141,  45), (147,  42)))
AreaManager.register(AreaInfo(u"北海道地方(南西部)", 203, (550, 455), ( 29,  84), (480, 387), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"東北地方(北部)",     204, (550, 455), ( 40,  17), (509, 421), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"東北地方(南部)",     205, (550, 455), ( 75,  25), (476, 430), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"関東地方",           206, (550, 455), ( 28,  58), (527, 362), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"甲信地方",           207, (550, 455), ( 29,   8), (524, 412), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"北陸地方(東部)",     208, (550, 455), ( 27,  84), (511, 388), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"北陸地方(西部)",     209, (550, 455), ( 17,  58), (510, 362), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"東海地方",           210, (550, 455), ( 74,  84), (494, 387), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"近畿地方",           211, (550, 455), ( 54,  93), (473, 396), (133,  36), (138,  33)))
AreaManager.register(AreaInfo(u"中国地方",           212, (550, 455), ( 26,   8), (529, 413), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"四国地方",           213, (550, 455), ( 45, 101), (469, 404), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"九州地方(北部)",     214, (550, 455), ( 51,  67), (477, 371), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"九州地方(南部)",     215, (550, 455), ( 91,  50), (527, 354), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"奄美地方",           216, (550, 455), ( 12,  67), (459, 370), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"沖縄本島地方",       217, (550, 455), ( 53,  50), (511, 354), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"大東島地方",         218, (550, 455), (  8,  33), (465, 337), (x, x), (x, x)))
AreaManager.register(AreaInfo(u"宮古・八重山地方",   219, (550, 455), ( 35,  84), (499, 387), (x, x), (x, x)))

# http://amayadori-opt.appspot.com/images/201/observed.png
# http://amayadori-opt.appspot.com/images/202/observed.png


if __name__ == "__main__":
  for area in AreaManager.areas:
    print area.code, area.name
    if area.glng1() > 0:
      print "N: " + str(area.glat1() + (area.gy1() * float(area.gdlat()) / area.gdy()))
      print "S: " + str(area.glat2() - ((area.dy() - area.gy2()) * float(area.gdlat()) / area.gdy()))
      print "W: " + str(area.glng1() - (area.gx1()               * float(area.gdlng()) / area.gdx()))
      print "E: " + str(area.glng2() + ((area.dx() - area.gx2()) * float(area.gdlng()) / area.gdx()))

#print AreaManager.find_by_code(211)
