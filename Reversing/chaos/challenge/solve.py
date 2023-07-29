import os
from gmpy2 import iroot
import re

# lazy solution
os.system("grep '__getitem__([0-9]*^[0-9]*).__pow__([0-9]*).__eq__([0-9]*)' chall.py -o > /tmp/res")

flag = [0 for n in range(51)]

for n in open("/tmp/res").readlines():
  x = re.findall("[0-9]*\^[0-9]*", n)[0]
  idx = int(x.split('^')[0]) ^ int(x.split('^')[1])
  p = int(re.findall("__pow__\([0-9]*\)", n)[0][8:-1])
  r = int(re.findall("__eq__\([0-9]*\)", n)[0][7:-1])
  flag[idx] = int(iroot(r,p)[0])

print(bytes(flag))
