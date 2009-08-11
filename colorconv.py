
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
  h(0x758DC9): water,
  h(0x7D9EC1): water,
  h(0x86A4CD): water,
  h(0x86A6D1): water,
  h(0x88A6CF): water,
  h(0x89AAD3): water,
  h(0x8AA9D2): water,
  h(0x8BABD1): water,
  h(0x8DACD2): water,
  h(0x8FADD2): water,
  h(0x90ADD3): water,
  h(0x91B0D2): water,
  h(0xB8B8E4): water,
  h(0xC0C0C0): water,
  h(0xC1C1C1): water,

  # 湖境界
  h(0x5C739F): water,
  h(0x5E759E): water,
  h(0x638099): water,
  h(0x648191): water,
  h(0x667D91): water,
  h(0x687F8F): water,
  h(0x6F8EA9): water,
  h(0x708AA2): water,
  h(0x708EAA): water,
  h(0x728D9F): water,
  h(0x728EA9): water,
  h(0x738DB7): water,
  h(0x7393B7): water,
  h(0x748FA9): water,
  h(0x748FAD): water,
  h(0x7692AF): water,
  h(0x7A9FA5): water,
  h(0x7D9DC2): water,
  h(0x7D9E8E): water,
  h(0x7E9CBB): water,
  h(0x7F9EC0): water,
  h(0x7F9EC2): water,
  h(0x809EAC): water,
  h(0x809EC0): water,
  h(0x89AAA8): water,
  h(0x8EADB4): water,
  h(0x90AFB7): water,
  h(0x97B5B4): water,
  h(0xD9D9D9): water,

  # 大地
  h(0x6D8D5E): ground,
  h(0x6D8E5F): ground,
  h(0x747B72): ground,
  h(0x749665): ground,
  h(0x759666): ground,
  h(0x769866): ground,
  h(0x769867): ground,
  h(0x769966): ground,
  h(0x779967): ground,
  h(0x779968): ground,
  h(0x789584): ground,
  h(0x789585): ground,
  h(0x799283): ground,
  h(0x7A9D6B): ground,
  h(0x7B9B88): ground,
  h(0x7D9E8E): ground,
  h(0x7DA16C): ground,
  h(0x7DA16D): ground,
  h(0x7E9E92): ground,
  h(0x7EA16D): ground,
  h(0x7FA26E): ground,
  h(0x7FA36F): ground,
  h(0x80A07E): ground,
  h(0x80A36F): ground,
  h(0x80A3A4): ground,
  h(0x819E92): ground,
  h(0x81A570): ground,
  h(0x82A37F): ground,
  h(0x82A571): ground,
  h(0x839F84): ground,
  h(0x84958A): ground,
  h(0x84A39B): ground,
  h(0x84A773): ground,
  h(0x84A873): ground,
  h(0x85A874): ground,
  h(0x86A975): ground,
  h(0x86A976): ground,
  h(0x87AA76): ground,
  h(0x87AA77): ground,
  h(0x88A89B): ground,
  h(0x88AB78): ground,
  h(0x89A99E): ground,
  h(0x89AAA8): ground,
  h(0x8AA486): ground,
  h(0x8AAC79): ground,
  h(0x8AAC7A): ground,
  h(0x8BACAC): ground,
  h(0x8BAD7A): ground,
  h(0x8CAD7C): ground,
  h(0x8CAE7D): ground,
  h(0x8CAF7C): ground,
  h(0x8DAAA6): ground,
  h(0x8DACA7): ground,
  h(0x8DAE7D): ground,
  h(0x8DAE7E): ground,
  h(0x8DAFAC): ground,
  h(0x8EAF7F): ground,
  h(0x8FAB88): ground,
  h(0x8FB080): ground,
  h(0x90AC89): ground,
  h(0x90B080): ground,
  h(0x90B081): ground,
  h(0x91B182): ground,
  h(0x92AE8F): ground,
  h(0x92B283): ground,
  h(0x93B283): ground,
  h(0x94B29A): ground,
  h(0x94B29C): ground,
  h(0x96B588): ground,
  h(0x97B588): ground,
  h(0x97B688): ground,
  h(0x99B7A5): ground,
  h(0x9CB98E): ground,
  h(0x9DB9AB): ground,
  h(0x9DBA8F): ground,
  h(0x9EB9BD): ground,
  h(0x9EBA90): ground,
  h(0x9FBB91): ground,
  h(0xA0BC93): ground,
  h(0xA1BD93): ground,
  h(0xA1BD94): ground,
  h(0xA1BD95): ground,
  h(0xA2BE95): ground,
  h(0xA2BE96): ground,
  h(0xA3BF97): ground,
  h(0xA4BF97): ground,
}

def color_conv(src):
  dst = imglib.RgbBitmap(src.width, src.height)

  missing = {}

  for y in xrange(src.height):
    for x in xrange(src.width):
      rgb1 = src.get_pixel(x, y)
      rgb2 = ctable.get(rgb1, (255, 128, 255))
      #rgb2 = ctable.get(rgb1, rgb1)
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
