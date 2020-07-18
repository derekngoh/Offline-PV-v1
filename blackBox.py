import binaryConvert as bc
from add_on import function_ops as fo
from add_on import cms_pad as cms
from add_on import rev_func_ops as revf

class BlackBox:
  """ 
  Stores encryption and decryption codes as well as default server login 
  email and password.
  """

  f = open(".keytext.txt", 'r')
  keytext = f.read()
  f.close()
  a = keytext
  def_email = a[195]+a[8]+a[3]+a[2]+a[27]+a[27]+a[2]+a[42]+a[1]+a[17]+a[23]+"@gmail.com"
  def_pass = a[195]+a[8]+a[3]+a[2]+a[27]+a[42].upper()+a[8]+a[3]+a[3]

  #makes the length of key same as the message.  
  def pad_key_to_blockbits(self, key, block_bits=64, char_bits=8):
    kmix = ord(key[0])+ord(key[1])+ord(key[-1])
    top_up_char = int(block_bits/char_bits)
    pad = self.keytext[len(key)+kmix:top_up_char+kmix]
    padded_key = key + pad

    return padded_key
 

  #encrypts message with same-length key and converts encrypted message into
  #binary string. Returns binary string of encrypted text.
  def encrypt(self, msg, key):
    padded_key = self.pad_key_to_blockbits(key)
    binary_padded_key = bc.conv_text_to_binary(padded_key)
    binary_message = bc.conv_text_to_binary(msg)

    cms_pad_64 = cms.CMS_pad_to_64bits(binary_message)
    final_cipher = fo.f_full(cms_pad_64, binary_padded_key) 

    return final_cipher

    
  #decrypts binary string message using key provided and converts binary into
  #text. If key is correct, decryption is correct. 
  def decrypt(self, enc_message, key, bits=8):
    padded_key = self.pad_key_to_blockbits(key)
    enc_message = enc_message.decode("ascii")
    binary_padded_key = bc.conv_text_to_binary(padded_key)

    bin_msg = revf.rev_f_full(enc_message, binary_padded_key)

    decoded_text = bc.conv_binary_to_text(bin_msg)
    remove_pad = decoded_text.replace("`", "")

    return remove_pad
