
# -*- coding: utf-8 -*-

import glob
import re

import png
import imglib
import ppmlib


water  = (0, 0, 0)
ground = (0, 64, 0)
ctable = {
  #(255,   0,   0): (255,   0,   0), # ‰J‰_    80mm/h ˆÈã
  #(255,   0, 255): (255,   0, 255), # ‰J‰_ 50-80mm/h
  #(255, 153,   0): (255, 153,   0), # ‰J‰_ 30-50mm/h
  #(255, 255,   0): (255, 255,   0), # ‰J‰_ 20-30mm/h
  #(  0, 255,   0): (  0, 255,   0), # ‰J‰_ 10-20mm/h
  #(  0,   0, 255): (  0,   0, 255), # ‰J‰_  5-10mm/h
  #( 51, 102, 255): ( 51, 102, 255), # ‰J‰_  1- 5mm/h
  #(153, 204, 255): (153, 204, 255), # ‰J‰_  0- 1mm/h

  # ƒJƒ‰[ƒe[ƒuƒ‹‚ÌŠm”F—p‚ÉAF‚ðŒ¸‚ç‚·
  (255,   0,   0): (  0,   0, 255), # ‰J‰_    80mm/h ˆÈã
  (255,   0, 255): (  0,   0, 255), # ‰J‰_ 50-80mm/h
  (255, 153,   0): (  0,   0, 255), # ‰J‰_ 30-50mm/h
  (255, 255,   0): (  0,   0, 255), # ‰J‰_ 20-30mm/h
  (  0, 255,   0): (  0,   0, 255), # ‰J‰_ 10-20mm/h
  (  0,   0, 255): (  0,   0, 255), # ‰J‰_  5-10mm/h
  ( 51, 102, 255): (  0,   0, 255), # ‰J‰_  1- 5mm/h
  (153, 204, 255): (  0,   0, 255), # ‰J‰_  0- 1mm/h

  ( 96,  57,  19): ground, # ŠÏ‘ª“_
  (230, 230, 230): (255, 255, 255), # “s“¹•{Œ§‹«ŠE
  (255, 255, 255): (255, 255, 255), # ŠCŠÝ‹«ŠE
  (102, 102, 102): (102, 102, 102), # ŠCŠÝ‹«ŠE/ƒOƒŠƒbƒh

  (116, 123, 114): (116, 123, 114), # ŠCŠÝ‹«ŠE
  (160, 160, 160): (160, 160, 160), # ŠCŠÝ‹«ŠE

  (117, 141, 201): water, # …–Ê
  (134, 164, 205): water, # …–Ê
  (134, 166, 209): water, # …–Ê
  (136, 166, 207): water, # …–Ê
  (141, 172, 210): water, # …–Ê
  (143, 173, 210): water, # …–Ê
  (144, 173, 211): water, # …–Ê
  (145, 176, 210): water, # …–Ê
  (184, 184, 228): water, # …–Ê
  (193, 193, 193): water, # …–Ê

  ( 92, 115, 159): water, # ŒÎ‹«ŠE
  ( 94, 117, 158): water, # ŒÎ‹«ŠE
  ( 99, 128, 153): water, # ŒÎ‹«ŠE
  (100, 129, 145): water, # ŒÎ‹«ŠE
  (102, 125, 145): water, # ŒÎ‹«ŠE
  (112, 138, 162): water, # ŒÎ‹«ŠE
  (112, 142, 170): water, # ŒÎ‹«ŠE
  (114, 141, 159): water, # ŒÎ‹«ŠE
  (114, 142, 169): water, # ŒÎ‹«ŠE
  (115, 141, 183): water, # ŒÎ‹«ŠE
  (115, 147, 183): water, # ŒÎ‹«ŠE
  (118, 146, 175): water, # ŒÎ‹«ŠE
  (125, 157, 194): water, # ŒÎ‹«ŠE
  (125, 158, 142): water, # ŒÎ‹«ŠE
  (126, 156, 187): water, # ŒÎ‹«ŠE
  (128, 158, 192): water, # ŒÎ‹«ŠE
  (137, 170, 168): water, # ŒÎ‹«ŠE
  (142, 173, 180): water, # ŒÎ‹«ŠE
  (151, 181, 180): water, # ŒÎ‹«ŠE

  (109, 141,  94): ground, # ‘å’n
  (109, 142,  95): ground, # ‘å’n
  (117, 150, 102): ground, # ‘å’n
  (118, 152, 102): ground, # ‘å’n
  (118, 153, 102): ground, # ‘å’n
  (119, 153, 103): ground, # ‘å’n
  (120, 149, 132): ground, # ‘å’n
  (122, 157, 107): ground, # ‘å’n
  (123, 155, 136): ground, # ‘å’n
  (125, 158, 142): ground, # ‘å’n
  (125, 161, 108): ground, # ‘å’n
  (125, 161, 109): ground, # ‘å’n
  (127, 162, 110): ground, # ‘å’n
  (127, 163, 111): ground, # ‘å’n
  (128, 163, 111): ground, # ‘å’n
  (128, 163, 164): ground, # ‘å’n
  (129, 158, 146): ground, # ‘å’n
  (129, 165, 112): ground, # ‘å’n
  (130, 165, 113): ground, # ‘å’n
  (132, 163, 155): ground, # ‘å’n
  (132, 167, 115): ground, # ‘å’n
  (132, 168, 115): ground, # ‘å’n
  (133, 168, 116): ground, # ‘å’n
  (134, 169, 117): ground, # ‘å’n
  (135, 170, 118): ground, # ‘å’n
  (135, 170, 119): ground, # ‘å’n
  (136, 168, 155): ground, # ‘å’n
  (136, 171, 120): ground, # ‘å’n
  (137, 169, 158): ground, # ‘å’n
  (137, 170, 168): ground, # ‘å’n
  (138, 172, 121): ground, # ‘å’n
  (139, 172, 172): ground, # ‘å’n
  (139, 173, 122): ground, # ‘å’n
  (140, 174, 125): ground, # ‘å’n
  (140, 175, 124): ground, # ‘å’n
  (141, 174, 126): ground, # ‘å’n
  (142, 175, 127): ground, # ‘å’n
  (143, 176, 128): ground, # ‘å’n
  (144, 172, 137): ground, # ‘å’n
  (144, 176, 128): ground, # ‘å’n
  (146, 174, 143): ground, # ‘å’n
  (146, 178, 131): ground, # ‘å’n
  (147, 178, 131): ground, # ‘å’n
  (148, 178, 156): ground, # ‘å’n
  (151, 181, 136): ground, # ‘å’n
  (151, 182, 136): ground, # ‘å’n
  (153, 183, 165): ground, # ‘å’n
  (156, 185, 142): ground, # ‘å’n
  (157, 186, 143): ground, # ‘å’n
  (158, 185, 189): ground, # ‘å’n
  (159, 187, 145): ground, # ‘å’n
  (161, 189, 147): ground, # ‘å’n
  (161, 189, 148): ground, # ‘å’n
  (162, 190, 149): ground, # ‘å’n
  (163, 191, 151): ground, # ‘å’n
  (164, 191, 151): ground, # ‘å’n
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


for infilepath in glob.glob("tmp/*.png")[0:2]:
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
