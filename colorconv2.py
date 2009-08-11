# -*- coding: utf-8 -*-

import glob
import re

import png
import imglib
import ppmlib

water   = 0x000000
water2  = 0x00FFFF # テスト用
ground  = 0x004000
ground2 = 0xFFFF00 # テスト用

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
  0x748CC8: water,
  0x7C7C7C: water,
  0x7C9CC0: water,
  0x808080: water,
  0x848484: water,
  0x84A4CC: water,
  0x84A4D0: water,
  0x888888: water,
  0x88A4CC: water,
  0x88A4D0: water,
  0x88A8D0: water,
  0x8C8C8C: water,
  0x8CA8D0: water,
  0x8CACD0: water,
  0x909090: water,
  0x90ACD0: water,
  0x90B0D0: water,
  0x949494: water,
  0x989898: water,
  0x9C9C9C: water,
  0xA4A4A4: water,
  0xA8A8A8: water,
  0xACACAC: water,
  0xB0B0B0: water,
  0xB4B4B4: water,
  0xB8B8B8: water,
  0xB8B8E4: water,
  0xBCBCBC: water,
  0xC0C0C0: water,

  # 湖境界
  0x587098: water,
  0x5C709C: water,
  0x5C70A4: water,
  0x5C7494: water,
  0x5C749C: water,
  0x608098: water,
  0x647C90: water,
  0x648090: water,
  0x687C8C: water,
  0x6880B8: water,
  0x6C84BC: water,
  0x6C8CA8: water,
  0x7088A0: water,
  0x7088C0: water,
  0x708C9C: water,
  0x708CA0: water,
  0x708CA8: water,
  0x708CB4: water,
  0x708CC0: water,
  0x7090B4: water,
  0x748CA8: water,
  0x748CAC: water,
  0x748CC0: water,
  0x7490AC: water,
  0x7894C4: water,
  0x789CA4: water,
  0x7C94B0: water,
  0x7C94C4: water,
  0x7C9C8C: water,
  0x7C9CB8: water,
  0x7C9CC0: water,
  0x809CAC: water,
  0x809CBC: water,
  0x809CC0: water,
  0x88A0D4: water,
  0x88A8A8: water,
  0x8CACB4: water,
  0x90ACB4: water,
  0x94B4B4: water,
  0x98B4B8: water,
  0xD8D8D8: water,

  # 大地
  0x385430: ground,
  0x4C6C3C: ground,
  0x547444: ground,
  0x5C7C4C: ground,
  0x607C50: ground,
  0x648454: ground,
  0x648854: ground,
  0x686868: ground,
  0x688858: ground,
  0x688C58: ground,
  0x6C8888: ground,
  0x6C8C5C: ground,
  0x6C905C: ground,
  0x6C9060: ground,
  0x708C60: ground,
  0x70905C: ground,
  0x709060: ground,
  0x709460: ground,
  0x747870: ground,
  0x749464: ground,
  0x749864: ground,
  0x749868: ground,
  0x789080: ground,
  0x789468: ground,
  0x789484: ground,
  0x789864: ground,
  0x789868: ground,
  0x78987C: ground,
  0x789888: ground,
  0x789C68: ground,
  0x789C6C: ground,
  0x7C8478: ground,
  0x7C9484: ground,
  0x7C9C68: ground,
  0x7C9C6C: ground,
  0x7C9C8C: ground,
  0x7C9C90: ground,
  0x7CA068: ground,
  0x7CA06C: ground,
  0x7CA46C: ground,
  0x80847C: ground,
  0x808C7C: ground,
  0x809078: ground,
  0x809C84: ground,
  0x809C8C: ground,
  0x809C90: ground,
  0x809C94: ground,
  0x80A06C: ground,
  0x80A070: ground,
  0x80A07C: ground,
  0x80A0A4: ground,
  0x80A46C: ground,
  0x80A470: ground,
  0x80A478: ground,
  0x848C7C: ground,
  0x849488: ground,
  0x84A074: ground,
  0x84A098: ground,
  0x84A470: ground,
  0x84A474: ground,
  0x84A870: ground,
  0x84A874: ground,
  0x84A878: ground,
  0x889880: ground,
  0x88A478: ground,
  0x88A47C: ground,
  0x88A484: ground,
  0x88A874: ground,
  0x88A878: ground,
  0x88A87C: ground,
  0x88A898: ground,
  0x88A89C: ground,
  0x88A8A8: ground,
  0x88AC74: ground,
  0x88AC78: ground,
  0x88AC7C: ground,
  0x88ACAC: ground,
  0x8C9C84: ground,
  0x8CA080: ground,
  0x8CA084: ground,
  0x8CA4A0: ground,
  0x8CA87C: ground,
  0x8CA880: ground,
  0x8CA888: ground,
  0x8CA8A4: ground,
  0x8CAC78: ground,
  0x8CAC7C: ground,
  0x8CAC80: ground,
  0x8CACA4: ground,
  0x8CACAC: ground,
  0x8CB07C: ground,
  0x8CB080: ground,
  0x90A484: ground,
  0x90AC80: ground,
  0x90AC84: ground,
  0x90AC88: ground,
  0x90AC8C: ground,
  0x90B080: ground,
  0x90B084: ground,
  0x90B480: ground,
  0x90B484: ground,
  0x94A48C: ground,
  0x94A888: ground,
  0x94A88C: ground,
  0x94AC88: ground,
  0x94B084: ground,
  0x94B088: ground,
  0x94B098: ground,
  0x94B09C: ground,
  0x94B480: ground,
  0x94B484: ground,
  0x94B488: ground,
  0x94B884: ground,
  0x989C98: ground,
  0x98B088: ground,
  0x98B08C: ground,
  0x98B488: ground,
  0x98B48C: ground,
  0x98B4A4: ground,
  0x98B884: ground,
  0x98B888: ground,
  0x98B88C: ground,
  0x98B890: ground,
  0x98BC88: ground,
  0x98BC8C: ground,
  0x9CAC90: ground,
  0x9CAC94: ground,
  0x9CB090: ground,
  0x9CB48C: ground,
  0x9CB490: ground,
  0x9CB88C: ground,
  0x9CB890: ground,
  0x9CB8A8: ground,
  0x9CB8BC: ground,
  0x9CBC8C: ground,
  0x9CBC90: ground,
  0xA0AC9C: ground,
  0xA0B098: ground,
  0xA0B494: ground,
  0xA0B498: ground,
  0xA0B894: ground,
  0xA0B898: ground,
  0xA0BC90: ground,
  0xA0BC94: ground,
  0xA4B498: ground,
  0xA4B4A0: ground,
  0xA4B898: ground,
  0xA4BC94: ground,
  0xA4C094: ground,
  0xA4C098: ground,
  0xA8B89C: ground,
  0xA8B8A0: ground,
  0xA8BC9C: ground,
  0xACB8A4: ground,
  0xB0B8B0: ground,
  0xB0BCA8: ground,
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
