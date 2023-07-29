from pwn import *
import random

i = 0

o = ""
def a(n):
  global o
  global i
  i += 1
  o += n
  o += "\n"

def pr(s: bytes):
  for n in s:
    r = random.randint(0,3)
    a(f"pushi {n}")
    a(f"popr {r}")
    a(f"pr {r}")

def read():
  a("pushi -1")
  a("popr 2")
  a("pushi 10")
  a("popr 1")
  a("in 0")
  a("pushr 0")
  a("cmp")
  a("pushi -12")
  a("popr 0")
  a("pushi 0")
  a("popr 1")
  a("pushi -12")
  a("popr 2")
  a("jmpc")

def build_num(n): # prereq: top of stack is 0
  if n<0:
    n = u32(p32(n, signed=True))
  n = bin(n)[2:].zfill(32)
  for i in range(32):
    a(f"ads {n[i]}")
    if i != 31:
      a(f"shs 1")

a("popr 0")
a("popr 0")
a("popr 0")
a("popr 1")
a("popr 0")
a("popr 2")
a("popr 2")
a("popr 2")
a("popr 2")
a("popr 2")
a("popr 2")
a("pushr 0")
a("pushr 1")
a("pushi 0")
build_num(0x10bede)
a("popr 1")
a("sub")
a("popr 1")
a("popr 1")
a("pushr 3")
a("raw 255 0")

open("asm", "w").write(o)
os.system("python3 compile.py")
