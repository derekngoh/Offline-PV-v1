import binaryConvert as bc

msg1 = '010001010110111001110100011001010111001000100000011000100110100101101110011000010111001001111001'
key = 'Orange'

"""
Takes a fixed length message and arbituary length key. Message encrypted with
padded key every 48 bits block via XOR operations. Returns XORed binary which  
is the compilation of all the blocks of 48 bits.

The reverse takes a fixed length ciphertext and decrypt key. Cipher text is
decrypted with key every 48 blocks via XOR operations. Returns original text 
in binary which is the compilation of the blocks of 48 bits.
"""

f = open(".keytext.txt", 'r')
keytext = f.read()
f.close()

#pad key to msg_bits. default set to 48 bits. 
#takes in key of any length of (default) 8 bit character
#returns key in binary of 48 bits
def pad_key_binary(key, msg_bits=48, char_bits=8):
  kmix = ord(key[0])+ord(key[1])+ord(key[-1])
  pad = keytext[len(key)+kmix:int(msg_bits/char_bits)+kmix]
  padded = key + pad
  aug_key = padded[:3]+padded[-4:-1]
  padded_bin = bc.conv_text_to_binary(aug_key)

  return padded_bin

#XOR input msg with key. returns ciphertext compiled every 48 bits (default)
def fixed_len_xor(msg_in_bin, key, msg_bits=48):
  padded_key = pad_key_binary(key)
  if len(padded_key) != msg_bits or (len(msg_in_bin)%msg_bits) != 0:
    raise Exception("FL xor length error. Check key and msg bit length. Should be 48 or multiples.")
  msg_part = msg_in_bin[:msg_bits]
  ciphertext = []
  if not msg_part:
    return ciphertext
  else:
    non_padded_xored_part = bin(int(msg_part,2)^int(padded_key,2))[2:]
    xored_part = ('%0'+ str(msg_bits) +'d') % int(non_padded_xored_part)
    ciphertext += [xored_part]
    msg_in_bin = msg_in_bin[msg_bits:]

    return ''.join(ciphertext) + ''.join(fixed_len_xor(msg_in_bin, key))

#XOR input with key. returns original text every 48 bits (default)
def rev_fixed_len_xor(ciphertext, key, msg_bits=48):
  padded_key = pad_key_binary(key)
  if len(padded_key) != msg_bits or (len(ciphertext)%msg_bits) != 0:
    raise Exception("fl rev xor length error. Check key and msg bit length. Should be 48 or multiples.")
  cipher_part = ciphertext[:msg_bits]
  msg = []
  if not cipher_part:
    return msg
  else:
    non_padded_rev_xor_part = bin(int(cipher_part,2)^int(padded_key,2))[2:]
    rev_xor_part = ('%0'+ str(msg_bits) +'d') % int(non_padded_rev_xor_part)
    msg += [rev_xor_part]
    ciphertext = ciphertext[msg_bits:]

    return ''.join(msg) + ''.join(rev_fixed_len_xor(ciphertext, key))

