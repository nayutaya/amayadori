# -*- coding: utf-8 -*-


class RadarImage:
  def __init__(self, image):
    self.image = image

  @staticmethod
  def dump(matrix, format = "%4.1f"):
    for row in matrix:
      print "| " + " ".join([format % val for val in row]) + " |"

  @staticmethod
  def color77(png, xy):
    sx, sy = xy
    return [[png.get_color((sx + x - 3, sy + y - 3)) for x in range(7)] for y in range(7)]


  @staticmethod
  def color_to_rain(color):
    table = {
      (255, 255, 255):  -1, # 海岸境界
      (230, 230, 230):  -1, # 都道府県境界
      (255,   0,   0): 120,
      (255,   0, 255):  80,
      (255, 153,   0):  50,
      (255, 255,   0):  30,
      (  0, 255,   0):  20,
      (  0,   0, 255):  10, # 5-10mm/h
      ( 51, 102, 255):   5, # 1-5mm/h
      (153, 204, 255):   1, # 0-1mm/h
    }
    return table.get(color, 0)

  @staticmethod
  def rain77(color77):
    return [[RadarImage.color_to_rain(color77[y][x]) for x in range(7)] for y in range(7)]

  @staticmethod
  def interpolate_by_around(src77):
    dst77 = [[float(src77[y][x]) for x in range(7)] for y in range(7)]

    for y in range(1, 6):
      for x in range(1, 6):
        if src77[y][x] < 0:
          points = []
          points.append(src77[y - 1][x - 1])
          points.append(src77[y - 1][x    ])
          points.append(src77[y - 1][x + 1])
          points.append(src77[y    ][x - 1])
          points.append(src77[y    ][x + 1])
          points.append(src77[y + 1][x - 1])
          points.append(src77[y + 1][x    ])
          points.append(src77[y + 1][x + 1])
          available_points = [val for val in points if val >= 0]
          if len(available_points) > 0:
            avg = float(sum(available_points)) / len(available_points)
          else:
            avg = 0
          dst77[y][x] = avg

    return dst77

  @staticmethod
  def crop(src77):
    return tuple([tuple([float(src77[y + 1][x + 1]) for x in range(5)]) for y in range(5)])

  @staticmethod
  def weighted_average55(value55, weight55):
    vwsum = 0.0
    wsum  = 0.0

    for y in range(5):
      for x in range(5):
         vwsum += value55[y][x] * weight55[y][x]
         wsum  += weight55[y][x]

    if wsum == 0.0: return 0.0
    return vwsum / wsum

  def get_rainfall(self, xy):
    cm = RadarImage.color77(self.image, xy)
    rm = RadarImage.rain77(cm)
    im = RadarImage.interpolate_by_around(rm)
    crm = RadarImage.crop(im)
    w55 = (
      (0.6, 0.7, 0.8, 0.7, 0.6),
      (0.7, 0.8, 0.9, 0.8, 0.7),
      (0.8, 0.9, 1.0, 0.9, 0.8),
      (0.7, 0.8, 0.9, 0.8, 0.7),
      (0.6, 0.7, 0.8, 0.7, 0.6))
    wm = RadarImage.weighted_average55(crm, w55)
    return wm


if __name__ == "__main__":
  w55 = (
    (0.6, 0.7, 0.8, 0.7, 0.6),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.8, 0.9, 1.0, 0.9, 0.8),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.6, 0.7, 0.8, 0.7, 0.6))
  RadarImage.dump(w55, "%i")
