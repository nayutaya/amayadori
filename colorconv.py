
# -*- coding: utf-8 -*-

import png
import imglib
import ppmlib

#file = open("00.png", "rb")
file = open("01.png", "rb")
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
  (255,   0,   0): (255,   0,   0), # 80mm/h �ȏ�
  (255,   0, 255): (255,   0, 255), # 50-80mm/h
  (255, 153,   0): (255, 153,   0), # 30-50mm/h
  (255, 255,   0): (255, 255,   0), # 20-30mm/h
  (  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  (153, 204, 255): (153, 204, 255), #  0- 1mm/h

  (255, 255, 255): (255, 255, 255), # �C�݋��E
  (230, 230, 230): (255, 255, 255), # �s���{�����E
  (102, 102, 102): (102, 102, 102), # �C�݋��E/�O���b�h

  (193, 193, 193): (193, 193, 193), # �ϑ��摜 �C
  (136, 166, 207): (136, 166, 207), # �ϑ��摜 ��
  (115, 141, 183): (115, 141, 183), # �ϑ��摜 �΋��E1
  ( 94, 117, 158): ( 94, 117, 158), # �ϑ��摜 �΋��E2
  (146, 178, 131): (146, 178, 131), # �ϑ��摜 ��n1
  (132, 167, 115): (132, 167, 115), # �ϑ��摜 ��n2

  (184, 184, 228): (184, 184, 228), # �\�z�摜 �C
  (134, 164, 205): (134, 164, 205), # �\�z�摜 ��1
  (144, 173, 211): (144, 173, 211), # �\�z�摜 ��2
  (184, 184, 228): (184, 184, 228), # �\�z�摜 ��3
  (117, 141, 201): (117, 141, 201), # �\�z�摜 ��4
  (114, 141, 159): (114, 141, 159), # �\�z�摜 �΋��E1
  ( 92, 115, 159): ( 92, 115, 159), # �\�z�摜 �΋��E2
  (159, 187, 145): (159, 187, 145), # �\�z�摜 ��n1
  (130, 165, 113): (130, 165, 113), # �\�z�摜 ��n2
  (143, 176, 128): (143, 176, 128), # �\�z�摜 ��n3
  (136, 171, 120): (136, 171, 120), # �\�z�摜 ��n4

  ( 96,  57,  19): ( 96,  57,  19), # �ϑ��_
}

for y in range(bitmap.height):
  for x in range(bitmap.width):
    rgb1 = bitmap.get_pixel(x, y)
    rgb2 = ctable.get(rgb1, (255, 128, 255))
    #if ctable.get(rgb1) == None:
    #  print "missing: " + repr(rgb1)
    bitmap.set_pixel(x, y, rgb2)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()
