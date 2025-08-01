from Crypto.Cipher import AES


class AESCipher:
  def __init__(self, key):
    self.key = str.encode(key)

  def encrypt(self, msg):
    cipher = AES.new(self.key, AES.MODE_ECB)
    cipherText = cipher.encrypt(str.encode(msg))
    return cipherText.hex()

  def decrypt(self, cipherText):
    decipher = AES.new(self.key, AES.MODE_ECB)
    msg = decipher.decrypt(bytes.fromhex(cipherText))
    return msg
