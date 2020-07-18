from add_on import xor_mod as xor
from add_on import expansion_mod as exp
from add_on import sbox_mod as sbox


def function_ops(ciphertext, key):
  #input ciphertext to be 32 bits
  #expands padded cipher (default fr 32 to 48 bits)
  expanded_cipher = exp.expand(ciphertext) 

  #xor expanded bits with key
  xor_exp_cipher = xor.fixed_len_xor(expanded_cipher, key)

  #reduce XORed bits (to default 32bits)
  final_cipher = sbox.sbox(xor_exp_cipher)

  return final_cipher


def f_net(tuple_LR, key, left_right_bits=32):
  left = tuple_LR[0]
  right = tuple_LR[1]

  if len(left) != len(right) or len(right) != left_right_bits:
    raise Exception("F_net input bit length error. Check length.")
  
  #left
  left_hs = right

  #right
  unpadded_right_hs = bin(int(left,2)^int(function_ops(right,key),2))[2:]
  right_hs = ("%0" + str(left_right_bits) + "d") % int(unpadded_right_hs)

  if len(left_hs) != len(str(right_hs)) or len(str(right_hs)) != left_right_bits:
    raise Exception("F_net output bit length error. Check length.")

  return left_hs + right_hs


def f_full(full_bin_msg, key, block_bits=64, f_rounds=16):
  cipher = []
  while len(full_bin_msg):
    try:
      msg_part = full_bin_msg[:block_bits]
    except:
      raise Exception("F_full input length error")

    for i in range(f_rounds):
      tuple_LR = (msg_part[:int(block_bits/2)], msg_part[int(block_bits/2):])
      msg_part = f_net(tuple_LR, key)
    cipher += msg_part 
    full_bin_msg = full_bin_msg[block_bits:]  
  
  return ''.join(cipher)
    
  
