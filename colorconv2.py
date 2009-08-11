# -*- coding: utf-8 -*-

import glob
import re

import png
import imglib
import ppmlib

water   = 0x000000
water2  = 0x00FFFF # テスト用
ground  = 0x004000
ground2 = 0x008000 # テスト用

translate_table = {
  #0xFC0000: 0xFF0000, # 雨雲    80mm/h 以上
  #0xFC00FC: 0xFF00FF, # 雨雲 50-80mm/h
  #0xFC9800: 0xFF9900, # 雨雲 30-50mm/h
  #0xFCFC00: 0xFFFF00, # 雨雲 20-30mm/h
  #0x00FC00: 0x00FF00, # 雨雲 10-20mm/h
  #0x0000FC: 0x0000FF, # 雨雲  5-10mm/h
  #0x3064FC: 0x3366FF, # 雨雲  1- 5mm/h
  #0x98CCFC: 0x99CCFF, # 雨雲  0- 1mm/h
  # カラーテーブルの確認用に、色を減らす
  0xFC0000: 0x0000FF, # 雨雲    80mm/h 以上
  0xFC00FC: 0x0000FF, # 雨雲 50-80mm/h
  0xFC9800: 0x0000FF, # 雨雲 30-50mm/h
  0xFCFC00: 0x0000FF, # 雨雲 20-30mm/h
  0x00FC00: 0x0000FF, # 雨雲 10-20mm/h
  0x0000FC: 0x0000FF, # 雨雲  5-10mm/h
  0x3064FC: 0x0000FF, # 雨雲  1- 5mm/h
  0x98CCFC: 0x0000FF, # 雨雲  0- 1mm/h

  0x603810: ground,   # 観測点
  0xE4E4E4: 0xFFFFFF, # 都道府県境界
  0xFCFCFC: 0xFFFFFF, # 海岸境界
  0x646464: 0x666666, # 海岸境界/グリッド
  0x747870: 0x747B72, # 海岸境界
  0xA0A0A0: 0xA0A0A0, # 海岸境界

  # 水面
  0x00748CC8: water,
  0x007C9CC0: water,
  0x0084A4CC: water,
  0x0084A4D0: water,
  0x0088A4CC: water,
  0x0088A4D0: water,
  0x0088A8D0: water,
  0x0088A4D0: water,
  0x0088A4D0: water,
  0x0088A8D0: water,
  0x0088A8D0: water,
  0x008CACD0: water,
  0x008CA8D0: water,
  0x008CACD0: water,
  0x0090ACD0: water,
  0x0090ACD0: water,
  0x0090B0D0: water,
  0x00B8B8E4: water,
  0x00C0C0C0: water,
  0x00C0C0C0: water,

  # 湖境界
  0x00587098: water,
  0x00587098: water,
  0x005C709C: water,
  0x005C709C: water,
  0x005C749C: water,
  0x005C7494: water,
  0x00608098: water,
  0x00648090: water,
  0x00647C90: water,
  0x00687C8C: water,
  0x006880B8: water,
  0x006C84BC: water,
  0x006C8CA8: water,
  0x007088A0: water,
  0x00708CA8: water,
  0x00708C9C: water,
  0x00708CA0: water,
  0x00708CA8: water,
  0x00708CB4: water,
  0x00708CC0: water,
  0x007090B4: water,
  0x00748CC0: water,
  0x00748CA8: water,
  0x00748CAC: water,
  0x007490AC: water,
  0x00789CA4: water,
  0x007894C4: water,
  0x007C9CC0: water,
  0x007C9C8C: water,
  0x007C94C4: water,
  0x007C9CB8: water,
  0x007C9CC0: water,
  0x007C9CC0: water,
  0x00809CBC: water,
  0x00809CAC: water,
  0x00809CC0: water,
  0x0088A8A8: water,
  0x008CACB4: water,
  0x0090ACB4: water,
  0x0094B4B4: water,
  0x0098B4B8: water,
  0x00D8D8D8: water,

  # 大地
  0x00688858: ground,
  0x006C8C5C: ground,
  0x006C8C5C: ground,
  0x006C9060: ground,
  0x006C905C: ground,
  0x00709460: ground,
  0x00747870: ground,
  0x00749464: ground,
  0x00749464: ground,
  0x00749864: ground,
  0x00749864: ground,
  0x00749864: ground,
  0x00749864: ground,
  0x00749864: ground,
  0x00749868: ground,
  0x00789484: ground,
  0x00789484: ground,
  0x00789864: ground,
  0x00789080: ground,
  0x00789C68: ground,
  0x00789C68: ground,
  0x00789888: ground,
  0x007C9C8C: ground,
  0x007CA06C: ground,
  0x007CA06C: ground,
  0x007CA06C: ground,
  0x007C9484: ground,
  0x007C9C90: ground,
  0x007CA06C: ground,
  0x007CA06C: ground,
  0x007CA06C: ground,
  0x00809C8C: ground,
  0x0080A07C: ground,
  0x0080A06C: ground,
  0x0080A0A4: ground,
  0x00809C84: ground,
  0x00809C90: ground,
  0x0080A470: ground,
  0x0080A07C: ground,
  0x0080A470: ground,
  0x0080A470: ground,
  0x00809C84: ground,
  0x0080A470: ground,
  0x00849488: ground,
  0x0084A098: ground,
  0x0084A470: ground,
  0x0084A870: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0084A874: ground,
  0x0088A898: ground,
  0x0088A878: ground,
  0x0088A89C: ground,
  0x0088A8A8: ground,
  0x0088A878: ground,
  0x0088AC78: ground,
  0x0088A484: ground,
  0x0088AC78: ground,
  0x0088AC78: ground,
  0x0088A878: ground,
  0x0088AC78: ground,
  0x0088ACAC: ground,
  0x0088AC78: ground,
  0x0088AC78: ground,
  0x008CA8A4: ground,
  0x008CAC7C: ground,
  0x008CAC7C: ground,
  0x008CAC7C: ground,
  0x008CA4A0: ground,
  0x008CA8A4: ground,
  0x008CACA4: ground,
  0x008CAC7C: ground,
  0x008CAC7C: ground,
  0x008CACAC: ground,
  0x008CB07C: ground,
  0x008CAC7C: ground,
  0x008CB07C: ground,
  0x008CA888: ground,
  0x008CB080: ground,
  0x008CB07C: ground,
  0x0090AC88: ground,
  0x0090B080: ground,
  0x0090B080: ground,
  0x0090B080: ground,
  0x0090AC8C: ground,
  0x0090B080: ground,
  0x0090B480: ground,
  0x0090B080: ground,
  0x0090B084: ground,
  0x0090B484: ground,
  0x0094B098: ground,
  0x0094B09C: ground,
  0x0094B484: ground,
  0x0094B488: ground,
  0x0094B488: ground,
  0x0094B488: ground,
  0x0098B888: ground,
  0x0098B488: ground,
  0x0098B488: ground,
  0x0098B4A4: ground,
  0x0098B888: ground,
  0x0098B88C: ground,
  0x009CB88C: ground,
  0x009CB8A8: ground,
  0x009CB88C: ground,
  0x009CB8BC: ground,
  0x009CB890: ground,
  0x009CB890: ground,
  0x009CB890: ground,
  0x00A0BC90: ground,
  0x00A0BC90: ground,
  0x00A0BC94: ground,
  0x00A0BC94: ground,
  0x00A0BC94: ground,
  0x00A0BC94: ground,
  0x00A0BC94: ground,
  0x00A0BC94: ground,
  0x00A4BC94: ground,
  0x00A4C094: ground,
}

def int_to_rgb(int):
  r = (0xFF0000 & int) >> 16
  g = (0x00FF00 & int) >> 8
  b = (0x0000FF & int) >> 0
  return (r, g, b)

def rgb_to_int(rgb):
  r, g, b = rgb
  int  = r << 16
  int |= g << 8
  int |= b << 0
  return int

def pngbin_to_bitmap(bin):
  pngimg = png.Png8bitPalette.load(bin)
  width  = pngimg.bitmap.width
  height = pngimg.bitmap.height

  bitmap = imglib.RgbBitmap(width, height)
  for y in xrange(height):
    for x in xrange(width):
      rgb = pngimg.get_color((x, y))
      bitmap.set_pixel(x, y, rgb)

  return bitmap

def read_png(path):
  file = open(path, "rb")
  bin = file.read()
  file.close()
  return pngbin_to_bitmap(bin)

def write_ppm(bitmap, path):
  file = open(path, "wb")
  ppm = ppmlib.PpmWriter(bitmap)
  ppm.write(file)
  file.close()

def rough(src):
  mask = int("11111100", 2)
  dst = imglib.RgbBitmap(src.width, src.height)
  for y in xrange(src.height):
    for x in xrange(src.width):
      r, g, b = src.get_pixel(x, y)
      dst.set_pixel(x, y, (r & mask, g & mask, b & mask))

  return dst

def translate(src):
  dst = imglib.RgbBitmap(src.width, src.height)
  for y in xrange(src.height):
    for x in xrange(src.width):
      rgb1 = src.get_pixel(x, y)
      color1 = rgb_to_int(rgb1)
      color2 = translate_table.get(color1)
      if color2 == None:
        #color2 = 0x000000
        color2 = 0xFF80FF
        #color2 = color1
      rgb2 = int_to_rgb(color2)
      dst.set_pixel(x, y, rgb2)
  return dst


for infilepath in glob.glob("tmp/*.png"):
  outfilepath = re.sub(r"^tmp\\", r"tmp2\\", re.sub(r"\.png$", r".ppm", infilepath))
  print infilepath
  print outfilepath

  bitmap1 = read_png(infilepath)
  bitmap2 = rough(bitmap1)
  bitmap3 = translate(bitmap2)
  write_ppm(bitmap3, outfilepath)
