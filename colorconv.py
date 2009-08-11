
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
  #(255,   0,   0): (255,   0,   0), # 80mm/h 以上
  #(255,   0, 255): (255,   0, 255), # 50-80mm/h
  #(255, 153,   0): (255, 153,   0), # 30-50mm/h
  #(255, 255,   0): (255, 255,   0), # 20-30mm/h
  #(  0, 255,   0): (  0, 255,   0), # 10-20mm/h
  #(  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  #( 51, 102, 255): ( 51, 102, 255), #  1- 5mm/h
  #(153, 204, 255): (153, 204, 255), #  0- 1mm/h

  # カラーテーブルの確認用に、色を減らす
  (255,   0,   0): (  0,   0, 255), # 80mm/h 以上
  (255,   0, 255): (  0,   0, 255), # 50-80mm/h
  (255, 153,   0): (  0,   0, 255), # 30-50mm/h
  (255, 255,   0): (  0,   0, 255), # 20-30mm/h
  (  0, 255,   0): (  0,   0, 255), # 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), #  5-10mm/h
  ( 51, 102, 255): (  0,   0, 255), #  1- 5mm/h
  (153, 204, 255): (  0,   0, 255), #  0- 1mm/h

  ( 96,  57,  19): ground, # 観測点
  (230, 230, 230): (255, 255, 255), # 都道府県境界
  (255, 255, 255): (255, 255, 255), # 海岸境界
  (102, 102, 102): (102, 102, 102), # 海岸境界/グリッド

  (116, 123, 114): (116, 123, 114), # 海岸境界
  (160, 160, 160): (160, 160, 160), # 海岸境界

  (117, 141, 201): water, # 水面
  (134, 164, 205): water, # 水面
  (134, 166, 209): water, # 水面
  (136, 166, 207): water, # 水面
  (141, 172, 210): water, # 水面
  (143, 173, 210): water, # 水面
  (144, 173, 211): water, # 水面
  (145, 176, 210): water, # 水面
  (184, 184, 228): water, # 水面
  (193, 193, 193): water, # 水面

  ( 92, 115, 159): water, # 湖境界
  ( 94, 117, 158): water, # 湖境界
  ( 99, 128, 153): water, # 湖境界
  (100, 129, 145): water, # 湖境界
  (102, 125, 145): water, # 湖境界
  (112, 138, 162): water, # 湖境界
  (112, 142, 170): water, # 湖境界
  (114, 141, 159): water, # 湖境界
  (114, 142, 169): water, # 湖境界
  (115, 141, 183): water, # 湖境界
  (115, 147, 183): water, # 湖境界
  (118, 146, 175): water, # 湖境界
  (125, 157, 194): water, # 湖境界
  (125, 158, 142): water, # 湖境界
  (126, 156, 187): water, # 湖境界
  (128, 158, 192): water, # 湖境界
  (137, 170, 168): water, # 湖境界
  (142, 173, 180): water, # 湖境界
  (151, 181, 180): water, # 湖境界

  (109, 141,  94): ground, # 大地
  (109, 142,  95): ground, # 大地
  (117, 150, 102): ground, # 大地
  (118, 152, 102): ground, # 大地
  (118, 153, 102): ground, # 大地
  (119, 153, 103): ground, # 大地
  (120, 149, 132): ground, # 大地
  (122, 157, 107): ground, # 大地
  (123, 155, 136): ground, # 大地
  (125, 158, 142): ground, # 大地
  (125, 161, 108): ground, # 大地
  (125, 161, 109): ground, # 大地
  (127, 162, 110): ground, # 大地
  (127, 163, 111): ground, # 大地
  (128, 163, 111): ground, # 大地
  (128, 163, 164): ground, # 大地
  (129, 158, 146): ground, # 大地
  (129, 165, 112): ground, # 大地
  (130, 165, 113): ground, # 大地
  (132, 163, 155): ground, # 大地
  (132, 167, 115): ground, # 大地
  (132, 168, 115): ground, # 大地
  (133, 168, 116): ground, # 大地
  (134, 169, 117): ground, # 大地
  (135, 170, 118): ground, # 大地
  (135, 170, 119): ground, # 大地
  (136, 168, 155): ground, # 大地
  (136, 171, 120): ground, # 大地
  (137, 169, 158): ground, # 大地
  (137, 170, 168): ground, # 大地
  (138, 172, 121): ground, # 大地
  (139, 172, 172): ground, # 大地
  (139, 173, 122): ground, # 大地
  (140, 174, 125): ground, # 大地
  (140, 175, 124): ground, # 大地
  (141, 174, 126): ground, # 大地
  (142, 175, 127): ground, # 大地
  (143, 176, 128): ground, # 大地
  (144, 172, 137): ground, # 大地
  (144, 176, 128): ground, # 大地
  (146, 174, 143): ground, # 大地
  (146, 178, 131): ground, # 大地
  (147, 178, 131): ground, # 大地
  (148, 178, 156): ground, # 大地
  (151, 181, 136): ground, # 大地
  (151, 182, 136): ground, # 大地
  (153, 183, 165): ground, # 大地
  (156, 185, 142): ground, # 大地
  (157, 186, 143): ground, # 大地
  (158, 185, 189): ground, # 大地
  (159, 187, 145): ground, # 大地
  (161, 189, 147): ground, # 大地
  (161, 189, 148): ground, # 大地
  (162, 190, 149): ground, # 大地
  (163, 191, 151): ground, # 大地
  (164, 191, 151): ground, # 大地
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
