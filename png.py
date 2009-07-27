# -*- coding: utf-8 -*-

import StringIO
import struct
import binascii
import zlib

class Utility:
  @staticmethod
  def crc32(bin):
    return struct.unpack("!L", struct.pack("!l", binascii.crc32(bin)))[0]


class Signature:
  Value1 = 0x89504E47
  Value2 = 0x0D0A1A0A

  @staticmethod
  def read(io):
    sig1 = struct.unpack("!L", io.read(4))[0]
    sig2 = struct.unpack("!L", io.read(4))[0]

    if sig1 != Signature.Value1 or sig2 != Signature.Value2:
      raise Exception, "invalid signature"

    return Signature()


class Chunk:
  def __init__(self, type, data = None):
    self.type = type
    self.data = data

  @staticmethod
  def read(io):
    length = struct.unpack("!L", io.read(4))[0]
    type   = io.read(4)
    data   = io.read(length)
    crc32  = struct.unpack("!L", io.read(4))[0]

    if crc32 != Utility.crc32(type + data):
      raise Exception, "CRC error"

    return Chunk(type = type, data = data)

  @staticmethod
  def read_to_end(io):
    chunks = []
    while True:
      chunk = Chunk.read(io)
      chunks.append(chunk)
      if chunk.type == "IEND":
        break
    return chunks


class Header:
  def __init__(self, width = 0, height = 0, bit_depth = 0, colour_type = 0, compression_method = 0, filter_method = 0, interlace_method = 0):
    self.width              = width
    self.height             = height
    self.bit_depth          = bit_depth
    self.colour_type        = colour_type
    self.compression_method = compression_method
    self.filter_method      = filter_method
    self.interlace_method   = interlace_method

  @staticmethod
  def read(io):
    header = Header()
    header.width              = struct.unpack("!L", io.read(4))[0]
    header.height             = struct.unpack("!L", io.read(4))[0]
    header.bit_depth          = struct.unpack("B",  io.read(1))[0]
    header.colour_type        = struct.unpack("B",  io.read(1))[0]
    header.compression_method = struct.unpack("B",  io.read(1))[0]
    header.filter_method      = struct.unpack("B",  io.read(1))[0]
    header.interlace_method   = struct.unpack("B",  io.read(1))[0]
    return header

  @staticmethod
  def load(bin):
    if len(bin) != 13:
      raise Exception, "invalid header"
    return Header.read(StringIO.StringIO(bin))


class Palette:
  def __init__(self, colors = []):
    self.colors = colors

  @staticmethod
  def read(io):
    colors = []
    while True:
      color = io.read(3)
      if len(color) == 0:
        break
      elif len(color) < 3:
        raise Exception, "invalid palette"
      colors.append(struct.unpack("BBB", color))
    return Palette(colors)

  @staticmethod
  def load(bin):
    if len(bin) % 3 != 0:
      raise Exception, "invalid palette"
    return Palette.read(StringIO.StringIO(bin))

  def dump(self):
    if len(self.colors) > 256:
      raise "palette too big"

    bin = ""
    for color in self.colors:
      bin += struct.pack("BBB", *color)
    return bin


class BitmapFor8bitPalette:
  def __init__(self, width = 0, height = 0, bitmap = []):
    self.width  = width
    self.height = height
    self.bitmap = bitmap

  @staticmethod
  def read(io, width, height):
    bitmap = []
    prev_line = [0 for x in range(width)]

    #print "---"
    for i in range(0, height):
      filter   = struct.unpack("B", io.read(1))[0]
      raw_line = struct.unpack(str(width) + "B", io.read(width))
      #if filter != 0: print ("filter", filter)
      #if filter != 0:
      #  raise Exception, "unsupported filter type: " + str(filter)
      if filter == 0: # None
        cur_line = list(raw_line)
        #print "raw:" + ",".join([("%02X" % char) for char in raw_line])
      elif filter == 1: # Sub
        cur_line = list(raw_line)
        for i in range(width - 1):
          if i == 0:
            cur_line[i] = cur_line[i] # no change
          else:
            cur_line[i] = (cur_line[i - 1] + cur_line[i]) % 256
        #print "raw:" + ",".join([str(char) for char in raw_line])
        #print "sub:" + ",".join([("%02X" % char) for char in cur_line])
      elif filter == 2: # Up
        cur_line = list(raw_line)
        for i in range(width - 1):
          if i == 0:
            cur_line[i] = cur_line[i] # no change
          else:
            cur_line[i] = (prev_line[i] + cur_line[i]) % 256
        #print "pre:" + ",".join([str(char) for char in prev_line])
        #print "raw:" + ",".join([str(char) for char in raw_line])
        #print "up_:" + ",".join([("%02X" % char) for char in cur_line])
      elif filter == 3: # Average
        cur_line = list(raw_line)
        for i in range(width - 1):
          if i == 0:
            cur_line[i] = cur_line[i] # no change
          else:
            cur_line[i] = (cur_line[i] + ((cur_line[i - 1] + prev_line[i]) / 2)) % 256
        #print "pre:" + ",".join([str(char) for char in prev_line])
        #print "raw:" + ",".join([str(char) for char in raw_line])
        #print "ave:" + ",".join([("%02X" % char) for char in cur_line])
      elif filter == 4: # Paeth
        cur_line = list(raw_line)
        for i in range(width - 1):
          if i == 0:
            cur_line[i] = cur_line[i] # no change
          else:
            a = cur_line[i - 1]
            b = prev_line[i]
            c = prev_line[i - 1]
            p = a + b - c
            pa = abs(p - a)
            pb = abs(p - b)
            pc = abs(p - c)
            if pa <= pb and pa <= pc: x = a
            elif pb <= pc: x = b
            else: x = c
            cur_line[i] = (cur_line[i] + x) % 256
        #print "pre:" + ",".join([str(char) for char in prev_line])
        #print "raw:" + ",".join([str(char) for char in raw_line])
        #print "pae:" + ",".join([("%02X" % char) for char in cur_line])
      else:
        raise Exception, "unsupported filter type: " + str(filter)
      bitmap.append(list(cur_line))
      prev_line = cur_line

    return BitmapFor8bitPalette(width, height, bitmap)

  @staticmethod
  def load(bin, width, height):
    if len(bin) != (width + 1) * height:
      raise Exception, "invalid bitmap"
    return BitmapFor8bitPalette.read(StringIO.StringIO(bin), width, height)


class PngContainer:
  def __init__(self, signature = None, chunks = None):
    self.signature = signature
    self.chunks    = chunks

  @staticmethod
  def read(io):
    container = PngContainer()
    container.signature = Signature.read(io)
    container.chunks    = Chunk.read_to_end(io)
    return container

  @staticmethod
  def load(bin):
    return PngContainer.read(StringIO.StringIO(bin))

  def chunks_by_type(self, type):
    return [chunk for chunk in self.chunks if chunk.type == type]

  def first_chunk_by_type(self, type):
    chunks = self.chunks_by_type(type)
    if len(chunks) == 0:
      raise Exception, "chunk not found"
    return chunks[0]

  def joined_chunk_by_type(self, type):
    chunks = self.chunks_by_type(type)
    if len(chunks) == 0:
      raise Exception, "chunk not found"

    joined_data = "".join([chunk.data for chunk in chunks])
    return Chunk(type = type, data = joined_data)


class Png8bitPalette:
  def __init__(self, palette = None, bitmap = None):
    self.palette = palette
    self.bitmap  = bitmap

  @staticmethod
  def read(io):
    container = PngContainer.read(io)

    header_chunk  = container.first_chunk_by_type("IHDR")
    header        = Header.load(header_chunk.data)
    if header.bit_depth          != 8: raise Exception, "unsupported bit depth"
    if header.colour_type        != 3: raise Exception, "unsupported colour type"
    if header.compression_method != 0: raise Exception, "unsupported compression method"
    if header.filter_method      != 0: raise Exception, "unsupported filter method"
    if header.interlace_method   != 0: raise Exception, "unsupported interlace method"

    palette_chunk = container.first_chunk_by_type("PLTE")
    palette       = Palette.load(palette_chunk.data)
    bitmap_chunk  = container.joined_chunk_by_type("IDAT")
    bitmap_data   = zlib.decompress(bitmap_chunk.data)
    bitmap        = BitmapFor8bitPalette.load(bitmap_data, header.width, header.height)

    return Png8bitPalette(palette = palette, bitmap = bitmap)

  @staticmethod
  def load(bin):
    return Png8bitPalette.read(StringIO.StringIO(bin))

  def get_palette_index(self, xy):
    x, y = xy
    return self.bitmap.bitmap[y][x]

  def get_color(self, xy):
    return self.palette.colors[self.get_palette_index(xy)]


if __name__ == "__main__":
  import png
  def png_to_ppm(png, filename):
    f = open(filename, "w")
    f.write("P3\n")
    f.write(str(png.bitmap.width) + " " + str(png.bitmap.height) + "\n")
    f.write("255\n")
    for y in range(png.bitmap.height):
      for x in range(png.bitmap.width):
        pi = png.get_palette_index((x, y))
        f.write(str(pi) + " " + str(pi) + " " + str(pi) + " ")
      f.write("\n")
    f.close()

  image1 = open("200907280255-00.png", "rb").read()
  #png1 = png.Png8bitPalette.load(image)
  png_to_ppm(png.Png8bitPalette.load(image1), "image1.ppm")

  image2 = open("200907280240-02.png", "rb").read()
  png_to_ppm(png.Png8bitPalette.load(image2), "image2.ppm")
