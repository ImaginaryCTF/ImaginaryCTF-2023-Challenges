#!/usr/bin/env python3
from pwn import *

flag = b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde'
parts = [u32(flag[i:i+4]) for i in range(0,len(flag),4)]

o = ""
for n in parts:
  a = n%2
  r = n
  r>>=1
  r += 64
  print(bin(n))
  print(bin(r))
  o += bytes.fromhex(hex(r)[2:].zfill(8)).hex()

print(bytes.fromhex(o))
print(o)
