"""
Takes an binary input of 32 bits and converts into an binary output of 48 bits
using an expansion table. Message padded using CMS syntax.
"""

exp_table = (32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,
  17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1)  
  
#Expand origin_bits(default 32) to exp_bits (default 48)
#Returns expanded binary message in 48 bits 
def expand(msg_in_binary, origin_bits=32, exp_bits=48):
  i = 0
  expanded_msg = []
  expanded_part = expanded_msg + (['']*exp_bits)

  if len(msg_in_binary) == 0:
    return expanded_msg
  else:
    msg = msg_in_binary[0:origin_bits]
    for i in range(len(expanded_part)):
      index = exp_table[int(i)]
      expanded_part[int(i)] = msg[index-1]

    expanded_msg += expanded_part
    expanded_part = expanded_msg + (['']*exp_bits)
    msg_in_binary = msg_in_binary[origin_bits:]

    return ''.join(expanded_msg) + ''.join(expand(msg_in_binary))

#Contract input binary cipher of exp_bits to contr_bits.
#Returns contracted binary message in 32 bits.
def contract(cipher_in_binary, contr_bits=32, exp_bits=48):
  if len(cipher_in_binary)%exp_bits != 0:
    raise Exception("Contract cipher length error. Check bits length.")
  contracted_msg = []
  contracted_part = contracted_msg + (['']*contr_bits)
  if len(cipher_in_binary) == 0:
    return contracted_msg
  else:
    cipher_part = cipher_in_binary[:exp_bits]
    for i in range(len(cipher_part)):
      if not contracted_part[exp_table[i]-1]:
        contracted_part[exp_table[i]-1] = cipher_part[i]
    contracted_msg += contracted_part
    cipher_in_binary = cipher_in_binary[exp_bits:]

    return ''.join(contracted_msg) + ''.join(contract(cipher_in_binary))     
        
