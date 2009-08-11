
# -*- coding: utf-8 -*-

import glob
import re

import png
import imglib
import ppmlib

def h(rgb):
  r = (0xFF0000 & rgb) >> 16
  g = (0x00FF00 & rgb) >> 8
  b = (0x0000FF & rgb) >> 0
  return (r, g, b)


water  = (0, 0, 0)
water2 = (0, 255, 255)
ground = (0, 64, 0)
ground2 = (0, 128, 0)

ctable = {
  #(255,   0,   0): (255,   0,   0), # 雨雲    80mm/h 以上
  #(255,   0, 255): (255,   0, 255), # 雨雲 50-80mm/h
  #(255, 153,   0): (255, 153,   0), # 雨雲 30-50mm/h
  #(255, 255,   0): (255, 255,   0), # 雨雲 20-30mm/h
  #(  0, 255,   0): (  0, 255,   0), # 雨雲 10-20mm/h
  #(  0,   0, 255): (  0,   0, 255), # 雨雲  5-10mm/h
  #( 51, 102, 255): ( 51, 102, 255), # 雨雲  1- 5mm/h
  #(153, 204, 255): (153, 204, 255), # 雨雲  0- 1mm/h

  # カラーテーブルの確認用に、色を減らす
  (255,   0,   0): (  0,   0, 255), # 雨雲    80mm/h 以上
  (255,   0, 255): (  0,   0, 255), # 雨雲 50-80mm/h
  (255, 153,   0): (  0,   0, 255), # 雨雲 30-50mm/h
  (255, 255,   0): (  0,   0, 255), # 雨雲 20-30mm/h
  (  0, 255,   0): (  0,   0, 255), # 雨雲 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), # 雨雲  5-10mm/h
  ( 51, 102, 255): (  0,   0, 255), # 雨雲  1- 5mm/h
  (153, 204, 255): (  0,   0, 255), # 雨雲  0- 1mm/h

  ( 96,  57,  19): ground, # 観測点
  (230, 230, 230): (255, 255, 255), # 都道府県境界
  (255, 255, 255): (255, 255, 255), # 海岸境界
  (102, 102, 102): (102, 102, 102), # 海岸境界/グリッド

  (116, 123, 114): (116, 123, 114), # 海岸境界
  (160, 160, 160): (160, 160, 160), # 海岸境界

  # 水面
  (117, 141, 201): water,
  (134, 164, 205): water,
  (134, 166, 209): water,
  (136, 166, 207): water,
  (141, 172, 210): water,
  (143, 173, 210): water,
  (144, 173, 211): water,
  (145, 176, 210): water,
  (184, 184, 228): water,
  (193, 193, 193): water,
  h(0x7D9EC1): water,
  h(0x89AAD3): water,
  h(0x8AA9D2): water,
  h(0x8BABD1): water,
  h(0xC0C0C0): water,

  # 湖境界
  ( 92, 115, 159): water,
  ( 94, 117, 158): water,
  ( 99, 128, 153): water,
  (100, 129, 145): water,
  (102, 125, 145): water,
  (112, 138, 162): water,
  (112, 142, 170): water,
  (114, 141, 159): water,
  (114, 142, 169): water,
  (115, 141, 183): water,
  (115, 147, 183): water,
  (118, 146, 175): water,
  (125, 157, 194): water,
  (125, 158, 142): water,
  (126, 156, 187): water,
  (128, 158, 192): water,
  (137, 170, 168): water,
  (142, 173, 180): water,
  (151, 181, 180): water,
  h(0x687F8F): water,
  h(0x6F8EA9): water,
  h(0x748FA9): water,
  h(0x748FAD): water,
  h(0x7A9FA5): water,
  h(0x7F9EC0): water,
  h(0x7F9EC2): water,
  h(0x809EAC): water,
  h(0x90AFB7): water,
  h(0xD9D9D9): water,

  # 大地
  (109, 141,  94): ground,
  (109, 142,  95): ground,
  (117, 150, 102): ground,
  (118, 152, 102): ground,
  (118, 153, 102): ground,
  (119, 153, 103): ground,
  (120, 149, 132): ground,
  (122, 157, 107): ground,
  (123, 155, 136): ground,
  (125, 158, 142): ground,
  (125, 161, 108): ground,
  (125, 161, 109): ground,
  (127, 162, 110): ground,
  (127, 163, 111): ground,
  (128, 163, 111): ground,
  (128, 163, 164): ground,
  (129, 158, 146): ground,
  (129, 165, 112): ground,
  (130, 165, 113): ground,
  (132, 163, 155): ground,
  (132, 167, 115): ground,
  (132, 168, 115): ground,
  (133, 168, 116): ground,
  (134, 169, 117): ground,
  (135, 170, 118): ground,
  (135, 170, 119): ground,
  (136, 168, 155): ground,
  (136, 171, 120): ground,
  (137, 169, 158): ground,
  (137, 170, 168): ground,
  (138, 172, 121): ground,
  (139, 172, 172): ground,
  (139, 173, 122): ground,
  (140, 174, 125): ground,
  (140, 175, 124): ground,
  (141, 174, 126): ground,
  (142, 175, 127): ground,
  (143, 176, 128): ground,
  (144, 172, 137): ground,
  (144, 176, 128): ground,
  (146, 174, 143): ground,
  (146, 178, 131): ground,
  (147, 178, 131): ground,
  (148, 178, 156): ground,
  (151, 181, 136): ground,
  (151, 182, 136): ground,
  (153, 183, 165): ground,
  (156, 185, 142): ground,
  (157, 186, 143): ground,
  (158, 185, 189): ground,
  (159, 187, 145): ground,
  (161, 189, 147): ground,
  (161, 189, 148): ground,
  (162, 190, 149): ground,
  (163, 191, 151): ground,
  (164, 191, 151): ground,
  h(0x747B72): ground,
  h(0x749665): ground,
  h(0x769867): ground,
  h(0x779968): ground,
  h(0x789585): ground,
  h(0x799283): ground,
  h(0x7E9E92): ground,
  h(0x7EA16D): ground,
  h(0x80A07E): ground,
  h(0x82A37F): ground,
  h(0x839F84): ground,
  h(0x84958A): ground,
  h(0x86A976): ground,
  h(0x8AA486): ground,
  h(0x8AAC7A): ground,
  h(0x8CAD7C): ground,
  h(0x8DAAA6): ground,
  h(0x8DACA7): ground,
  h(0x8DAE7D): ground,
  h(0x8DAFAC): ground,
  h(0x8FAB88): ground,
  h(0x90B081): ground,
  h(0x91B182): ground,
  h(0x94B29A): ground,
  h(0x96B588): ground,
  h(0x9DB9AB): ground,
  h(0x9EBA90): ground,
  h(0xA0BC93): ground,
  h(0xA1BD95): ground,
  h(0xA2BE96): ground,
}

def color_conv(src):
  dst = imglib.RgbBitmap(src.width, src.height)

  missing = {}

  for y in xrange(src.height):
    for x in xrange(src.width):
      rgb1 = src.get_pixel(x, y)
      #rgb2 = ctable.get(rgb1, (255, 128, 255))
      rgb2 = ctable.get(rgb1, rgb1)
      if ctable.get(rgb1) == None:
        missing[rgb1] = missing.get(rgb1, 0) + 1

      dst.set_pixel(x, y, rgb2)

  return dst


for infilepath in glob.glob("tmp/*.png"):
  outfilepath = re.sub(r"^tmp\\", r"tmp2\\", re.sub(r"\.png$", r".ppm", infilepath))
  print infilepath
  print outfilepath

  infile = open(infilepath, "rb")
  infilebin = infile.read()
  infile.close()

  pngimg = png.Png8bitPalette.load(infilebin)
  width  = pngimg.bitmap.width
  height = pngimg.bitmap.height

  bitmap = imglib.RgbBitmap(width, height)
  for y in range(height):
    for x in range(width):
      rgb = pngimg.get_color((x, y))
      bitmap.set_pixel(x, y, rgb)

  bitmap2 = color_conv(bitmap)

  outfile = open(outfilepath, "wb")
  ppm = ppmlib.PpmWriter(bitmap2)
  ppm.write(outfile)
  outfile.close()

  #break


"""
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
"""
