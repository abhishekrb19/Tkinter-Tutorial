from bitarray import bitarray
bit_array = bitarray(128)
bit_array.setall(0)
bit_array[125] = 0
bit_array[1] = 1
bit_array[3] = 1

print bit_array

# for b in bit_array:
#     print b
# print int(bit_array)

# print bit_array.decode()

aa = [0] * 128
aa[10] = 1 # choose bin num 10
aa[12] = 1 # choose bin num 12
aa[2] = 1
aa[3] = 1
#aa[5] = 1

def shifting(bitlist):
     out = 0
     for bit in reversed(bitlist):
         out = (out << 1) | bit
     return out
print shifting(bit_array)
print shifting(aa)