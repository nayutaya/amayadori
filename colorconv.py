
# -*- coding: utf-8 -*-

import png
import imglib
import ppmlib

#file = open("00.png", "rb")
file = open("200908111540-02.png", "rb")
bin  = file.read()
png  = png.Png8bitPalette.load(bin)
width  = png.bitmap.width
height = png.bitmap.height

bitmap = imglib.RgbBitmap(width, height)
for y in range(height):
  for x in range(width):
    rgb = png.get_color((x, y))
    bitmap.set_pixel(x, y, rgb)

water  = (0, 0, 0)
ground = (0, 64, 0)

ctable = {
  #(255,   0,   0): (255,   0,   0), # 80mm/h �ȏ�
  #(255,   0, 255): (255,   0, 255), # 50-80mm/h
  #(255, 153,   0): (255, 153,   0), # 30-50mm/h
  #(255, 255,   0): (255, 255,   0), # 20-30mm/h
  #(  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  #(  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  #( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  #(153, 204, 255): (153, 204, 255), #  0- 1mm/h

  # �J���[�e�[�u���̊m�F�p�ɁA�F�����炷
  (255,   0,   0): (  0,   0, 255), # 80mm/h �ȏ�
  (255,   0, 255): (  0,   0, 255), # 50-80mm/h
  (255, 153,   0): (  0,   0, 255), # 30-50mm/h
  (255, 255,   0): (  0,   0, 255), # 20-30mm/h
  (  0, 255,   0): (  0,   0, 255), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): (  0,   0, 255), #  1- 5mm/h
  (153, 204, 255): (  0,   0, 255), #  0- 1mm/h

  ( 96,  57,  19): ground, # �ϑ��_
  (230, 230, 230): (255, 255, 255), # �s���{�����E
  (255, 255, 255): (255, 255, 255), # �C�݋��E
  (102, 102, 102): (102, 102, 102), # �C�݋��E/�O���b�h

  (116, 123, 114): (116, 123, 114), # �C�݋��E
  (160, 160, 160): (160, 160, 160), # �C�݋��E

  (117, 141, 201): water, # ����
  (134, 164, 205): water, # ����
  (134, 166, 209): water, # ����
  (136, 166, 207): water, # ����
  (141, 172, 210): water, # ����
  (143, 173, 210): water, # ����
  (144, 173, 211): water, # ����
  (145, 176, 210): water, # ����
  (184, 184, 228): water, # ����
  (193, 193, 193): water, # ����

  ( 92, 115, 159): water, # �΋��E
  ( 94, 117, 158): water, # �΋��E
  ( 99, 128, 153): water, # �΋��E
  (100, 129, 145): water, # �΋��E
  (102, 125, 145): water, # �΋��E
  (112, 138, 162): water, # �΋��E
  (112, 142, 170): water, # �΋��E
  (114, 141, 159): water, # �΋��E
  (114, 142, 169): water, # �΋��E
  (115, 141, 183): water, # �΋��E
  (115, 147, 183): water, # �΋��E
  (118, 146, 175): water, # �΋��E
  (125, 157, 194): water, # �΋��E
  (125, 158, 142): water, # �΋��E
  (126, 156, 187): water, # �΋��E
  (128, 158, 192): water, # �΋��E
  (137, 170, 168): water, # �΋��E
  (142, 173, 180): water, # �΋��E
  (151, 181, 180): water, # �΋��E

  (109, 141,  94): ground, # ��n
  (109, 142,  95): ground, # ��n
  (117, 150, 102): ground, # ��n
  (118, 152, 102): ground, # ��n
  (118, 153, 102): ground, # ��n
  (119, 153, 103): ground, # ��n
  (120, 149, 132): ground, # ��n
  (122, 157, 107): ground, # ��n
  (123, 155, 136): ground, # ��n
  (125, 158, 142): ground, # ��n
  (125, 161, 108): ground, # ��n
  (125, 161, 109): ground, # ��n
  (127, 162, 110): ground, # ��n
  (127, 163, 111): ground, # ��n
  (128, 163, 111): ground, # ��n
  (128, 163, 164): ground, # ��n
  (129, 158, 146): ground, # ��n
  (129, 165, 112): ground, # ��n
  (130, 165, 113): ground, # ��n
  (132, 163, 155): ground, # ��n
  (132, 167, 115): ground, # ��n
  (132, 168, 115): ground, # ��n
  (133, 168, 116): ground, # ��n
  (134, 169, 117): ground, # ��n
  (135, 170, 118): ground, # ��n
  (135, 170, 119): ground, # ��n
  (136, 168, 155): ground, # ��n
  (136, 171, 120): ground, # ��n
  (137, 169, 158): ground, # ��n
  (137, 170, 168): ground, # ��n
  (138, 172, 121): ground, # ��n
  (139, 172, 172): ground, # ��n
  (139, 173, 122): ground, # ��n
  (140, 174, 125): ground, # ��n
  (140, 175, 124): ground, # ��n
  (141, 174, 126): ground, # ��n
  (142, 175, 127): ground, # ��n
  (143, 176, 128): ground, # ��n
  (144, 172, 137): ground, # ��n
  (144, 176, 128): ground, # ��n
  (146, 174, 143): ground, # ��n
  (146, 178, 131): ground, # ��n
  (147, 178, 131): ground, # ��n
  (148, 178, 156): ground, # ��n
  (151, 181, 136): ground, # ��n
  (151, 182, 136): ground, # ��n
  (153, 183, 165): ground, # ��n
  (156, 185, 142): ground, # ��n
  (157, 186, 143): ground, # ��n
  (158, 185, 189): ground, # ��n
  (159, 187, 145): ground, # ��n
  (161, 189, 147): ground, # ��n
  (161, 189, 148): ground, # ��n
  (162, 190, 149): ground, # ��n
  (163, 191, 151): ground, # ��n
  (164, 191, 151): ground, # ��n
}

missing = {}

for y in range(bitmap.height):
  for x in range(bitmap.width):
    rgb1 = bitmap.get_pixel(x, y)
    rgb2 = ctable.get(rgb1, (255, 128, 255))
    #rgb2 = ctable.get(rgb1, rgb1)
    if ctable.get(rgb1) == None:
      missing[rgb1] = missing.get(rgb1, 0) + 1

    bitmap.set_pixel(x, y, rgb2)

outfile = open("tmp.ppm", "wb")
ppm = ppmlib.PpmWriter(bitmap)
ppm.write(outfile)
outfile.close()

def cmp(a, b):
  argb, ac = a
  brgb, bc = b
  return ac - bc
missing = missing.items()
missing.sort(cmp)
for (rgb, count) in missing:
  r, g, b = rgb
  #if g > r and g > b:
  if b > r and b > g:
    print (rgb, count)
