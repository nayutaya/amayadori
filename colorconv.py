
# -*- coding: utf-8 -*-

import png
import imglib
import ppmlib

file = open("00.png", "rb")
#file = open("01.png", "rb")
bin  = file.read()
png  = png.Png8bitPalette.load(bin)
width  = png.bitmap.width
height = png.bitmap.height

bitmap = imglib.RgbBitmap(width, height)
for y in range(height):
  for x in range(width):
    rgb = png.get_color((x, y))
    bitmap.set_pixel(x, y, rgb)

ctable = {
  (255,   0,   0): (255,   0,   0), # 80mm/h à»è„
  (255,   0, 255): (255,   0, 255), # 50-80mm/h
  (255, 153,   0): (255, 153,   0), # 30-50mm/h
  (255, 255,   0): (255, 255,   0), # 20-30mm/h
  (  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  (153, 204, 255): (153, 204, 255), #  0- 1mm/h

  (255, 255, 255): (255, 255, 255), # äCä›ã´äE
  (230, 230, 230): (255, 255, 255), # ìsìπï{åßã´äE
}

for y in range(bitmap.height):
  for x in range(bitmap.width):
    rgb1 = bitmap.get_pixel(x, y)
    rgb2 = ctable.get(rgb1, (0, 0, 0))
    bitmap.set_pixel(x, y, rgb2)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()
