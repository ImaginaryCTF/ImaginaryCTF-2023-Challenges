from PIL import Image
import random

o = Image.open("./original.png")
n = Image.open("./chall.png")
op = o.load()
np = n.load()

out = ""
for i in range(o.size[0]):
  for j in range(o.size[1]):
    if np[i,j][2] - op[i,j][2] == 1:
      out += str(np[i,j][0] - op[i,j][0])

print(bytes.fromhex(hex(int(out,2))[2:]))
