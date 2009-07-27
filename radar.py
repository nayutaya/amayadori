# -*- coding: utf-8 -*-

class RadarImage:
  color_table = {
    (255, 255, 255):  -1, # 海岸境界
    (230, 230, 230):  -1, # 都道府県境界
    (255,   0,   0): 120, # 80mm/h 以上
    (255,   0, 255):  80, # 50-80mm/h
    (255, 153,   0):  50, # 30-50mm/h
    (255, 255,   0):  30, # 20-30mm/h
    (  0, 255,   0):  20, # 10-20mm/h
    (  0,   0, 255):  10, #  5-10mm/h
    ( 51, 102, 255):   5, #  1- 5mm/h
    (153, 204, 255):   1, #  0- 1mm/h
  }

  weight_matrix = (
    (0.6, 0.7, 0.8, 0.7, 0.6),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.8, 0.9, 1.0, 0.9, 0.8),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.6, 0.7, 0.8, 0.7, 0.6))

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
    return RadarImage.color_table.get(color, 0)

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

  def get_average_rainfall(self, xy):
    color_matrix                 = RadarImage.color77(self.image, xy)
    raw_rainfall_matrix          = RadarImage.rain77(color_matrix)
    interpolated_rainfall_matrix = RadarImage.interpolate_by_around(raw_rainfall_matrix)
    cropped_rainfall_matrix      = RadarImage.crop(interpolated_rainfall_matrix)

    return RadarImage.weighted_average55(cropped_rainfall_matrix, RadarImage.weight_matrix)

  def ballpark_rainfall(self, rainfall):
    if rainfall < 0: return 0
    list = [(value, abs(rainfall - value)) for value in [0, 1, 5, 10, 20, 30, 50, 80, 120]]
    def cmp(a, b):
      value1, distance1 = a
      value2, distance2 = b
      if distance1 > distance2: return 1
      if distance1 < distance2: return -1
      if value1 > value2: return 1
      if value1 < value2: return -1
      return 0
    list.sort(cmp)
    return list[0][0]

  def get_ballpark_rainfall(self, xy):
    return self.ballpark_rainfall(self.get_average_rainfall(xy))


if __name__ == "__main__":
  """
  w55 = (
    (0.6, 0.7, 0.8, 0.7, 0.6),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.8, 0.9, 1.0, 0.9, 0.8),
    (0.7, 0.8, 0.9, 0.8, 0.7),
    (0.6, 0.7, 0.8, 0.7, 0.6))
  RadarImage.dump(w55, "%i")
  """
  r = RadarImage(None)
  print r.ballpark_rainfall(-1.0)
  print r.ballpark_rainfall(0.0)
  print r.ballpark_rainfall(0.5)
  print r.ballpark_rainfall(0.9)
  print r.ballpark_rainfall(2.0)
  print r.ballpark_rainfall(9.0)
  print r.ballpark_rainfall(11.0)
  print r.ballpark_rainfall(21.0)
  print r.ballpark_rainfall(41.0)
  print r.ballpark_rainfall(70.0)
  print r.ballpark_rainfall(100.0)
