import cv2
from tkinter import messagebox


class AppError(BaseException):
  pass

c=0

def i2bin(i, l):
  actual = bin(i)[2:]


  while len(actual) < l:
    actual = "0"+actual

  return actual


def char2bin(c):
  return i2bin(ord(c), 8)


class LSB():
  MAX_BIT_LENGTH = 16
  enc = '0'

  def __init__(self, img):
    self.size_x, self.size_y, self.size_channel = img.shape
    self.imageCapacity = self.size_x * self.size_x * self.size_channel
    self.image = img
    self.cur_x = 0
    self.cur_y = 0
    self.cur_channel = 0

  def next(self):
    if self.cur_channel != self.size_channel-1:
      self.cur_channel += 1
    else:
      self.cur_channel = 0
      if self.cur_y != self.size_y-1:
        self.cur_y += 1
      else:
        self.cur_y = 0
        if self.cur_x != self.size_x-1:
          self.cur_x += 1


  def put_bit(self, bit):
    v = self.image[self.cur_x, self.cur_y][self.cur_channel]
    binaryV = bin(v)[2:]
    if binaryV[-1] != bit:
      binaryV = binaryV[:-1]+bit
    self.image[self.cur_x, self.cur_y][self.cur_channel] = int(binaryV,2)
    self.next()

  def put_bits(self, bits):
    for bit in bits:
      self.put_bit(bit)

  def read_bit(self):
    v = self.image[self.cur_x, self.cur_y][self.cur_channel]
    return bin(v)[-1]

  def read_bits(self, length):
    bits = ""
    for _ in range(0, length):
      bits += self.read_bit()
      self.next()

    return bits

  def embed(self, text):
    try:
      a = bin(len(text))[2:]
      if len(a) > self.MAX_BIT_LENGTH:
        messagebox.showinfo("Info", "bit size is larger than expected.")
        self.enc ='1'
      text_length = i2bin(len(text), self.MAX_BIT_LENGTH)
      self.put_bits(text_length)
      for c in text:
        bits = char2bin(c)
        self.put_bits(bits)
      if self.enc == '0':
        messagebox.showinfo("Info", "Encoded")
    except ValueError:
      messagebox.showwarning("Warning", "Reduce message size!")

  def extract(self):
    length = int(self.read_bits(self.MAX_BIT_LENGTH), 2)
    text = ""
    for _ in range(0, length):
      c = int(self.read_bits(8), 2)
      text += chr(c)

    return text

  def save(self, dstPath):
    cv2.imwrite(dstPath, self.image)
