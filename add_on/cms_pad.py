import binaryConvert as bc

#Pad message to block bits (default 64) using CMS syntax.
#returns tuple of Left 32 bits, Right 32bits

def CMS_pad_to_64bits(msg, block_bits=64, char_bits=8):
  if len(msg) <= block_bits:
    bits_to_pad = block_bits - len(msg)
  else:
    bits_to_pad = block_bits-len(msg)%block_bits
  num_of_char = int(bits_to_pad/char_bits)
  bin_pad = bc.conv_text_to_binary('`') * num_of_char

  msg += bin_pad

  return msg
