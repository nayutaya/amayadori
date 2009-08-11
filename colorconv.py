
# -*- coding: utf-8 -*-

import png
import imglib
import ppmlib

file = open("00.png", "rb")
bin  = file.read()
png  = png.Png8bitPalette.load(bin)
width  = png.bitmap.width
height = png.bitmap.height

bitmap = imglib.RgbBitmap(width, height)
for y in range(height):
  for x in range(width):
    rgb = png.get_color((x, y))
    bitmap.set_pixel(x, y, rgb)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()
