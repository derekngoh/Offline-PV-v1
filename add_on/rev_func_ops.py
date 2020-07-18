from add_on.function_ops import function_ops as fops

def rev_f_net(tuple_LR, key, left_right_bits=32):
  left = tuple_LR[0]
  right = tuple_LR[1]

  if len(left) != len(right) or len(right) != left_right_bits:
    raise Exception("rev_f_net input bit length error. Check length.")

  #right
  right_hs = left

  #left
  unpadded_left_hs = bin(int(right, 2) ^ int(fops(left, key), 2))[2:]
  left_hs = ("%0" + str(left_right_bits) + "d") % int(unpadded_left_hs)

  if len(left_hs) != len(str(right_hs)) or len(str(right_hs)) != left_right_bits:
    raise Exception("rev_f_net output bit length error. Check length.")

  return left_hs + right_hs


def rev_f_full(full_cipher, key, block_bits=64, f_rounds=16):
  msg = []
  while len(full_cipher):
    try:
      cipher_part = full_cipher[:block_bits]
    except:
      raise Exception("rev_f_full input length error")

    for i in range(f_rounds):
      tuple_LR = (cipher_part[:int(block_bits/2)], cipher_part[int(block_bits/2):])
      cipher_part = rev_f_net(tuple_LR, key)
    
    msg += cipher_part  
    full_cipher = full_cipher[block_bits:]

  return ''.join(msg)
