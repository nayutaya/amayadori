
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
  (255,   0,   0): (255,   0,   0), # 80mm/h ˆÈã
  (255,   0, 255): (255,   0, 255), # 50-80mm/h
  (255, 153,   0): (255, 153,   0), # 30-50mm/h
  (255, 255,   0): (255, 255,   0), # 20-30mm/h
  (  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  (153, 204, 255): (153, 204, 255), #  0- 1mm/h

  (255, 255, 255): (255, 255, 255), # ŠCŠİ‹«ŠE
  (230, 230, 230): (255, 255, 255), # “s“¹•{Œ§‹«ŠE

  (193, 193, 193): (193, 193, 193), # ŠÏ‘ª‰æ‘œ ŠC
  (102, 102, 102): (102, 102, 102), # ƒOƒŠƒbƒh/ŠCŠİ‹«ŠE

  (146, 178, 131): (146, 178, 131), # ‘å’n1
  (132, 167, 115): (132, 167, 115), # ‘å’n2

  (136, 166, 207): (136, 166, 207), # ŒÎ
  (115, 141, 183): (115, 141, 183), # ŒÎ‹«ŠE1
  ( 94, 117, 158): ( 94, 117, 158), # ŒÎ‹«ŠE2

  ( 96,  57,  19): ( 96,  57,  19), # ŠÏ‘ª“_
}

for y in range(bitmap.height):
  for x in range(bitmap.width):
    rgb1 = bitmap.get_pixel(x, y)
    rgb2 = ctable.get(rgb1, (255, 128, 255))
    bitmap.set_pixel(x, y, rgb2)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()
