import random


mybits = random.getrandbits(4)
mybits_bin = bin(mybits)
#print(len(mybits_bin))
#print(mybits_bin[2:].rjust(4, '0'))
#bytes_to_write = bytearray([mybits for i in range(10)])
#print(bytes_to_write)
numb = 50 # dec: 50 -> hex: 32
numb2 = 57
print(f"Numero {numb} en binario {numb.to_bytes()} y en char {chr(0x32)}")

