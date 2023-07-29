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

def fail():
  target = 0xf000
  a("pushi 0")
  a("popr 1")
  a("pushi 0")
  build_num(target)
  a("popr 0")
  a("jmp 0")

def cmp(t):
  c1 = random.randint(0,64)
  c2 = random.randint(1,127)
  a("popr 1")
  a(f"pushi {c1}")
  a("popr 0")
  a("add")
  a("pushr 3")
  a("popr 0")
  a(f"pushi {c2}")
  a("popr 1")
  a("mul")
  a("pushi 0")
  build_num((t+c1)*c2)
  a("popr 1")
  a("pushr 3")
  a("popr 0")
  a("cmp")
  a("pushi 0")
  build_num(68)
  a("popr 1")
  a("pushi 0")
  a("popr 0")
  a("pushi 0")
  a("popr 2")
  a("jmpc")
  fail()

pr(r"""                                  |>>>
                                  |
                    |>>>      _  _|_  _         |>>>
                    |        |;| |;| |;|        |
                _  _|_  _    \\.    .  /    _  _|_  _
               |;|_|;|_|;|    \\:. ,  /    |;|_|;|_|;|
               \\..      /    ||;   . |    \\.    .  /
                \\.  ,  /     ||:  .  |     \\:  .  /
                 ||:   |_   _ ||_ . _ | _   _||:   |
                 ||:  .|||_|;|_|;|_|;|_|;|_|;||:.  |
                 ||:   ||.    .     .      . ||:  .|
                 ||: . || .     . .   .  ,   ||:   |       \,/
                 ||:   ||:  ,  _______   .   ||: , |            /`\
                 ||:   || .   /+++++++\    . ||:   |
                 ||:   ||.    |+++++++| .    ||: . |
              __ ||: . ||: ,  |+++++++|.  . _||_   |
     ____--`~    '--~~__|.    |+++++__|----~    ~`---,              ___
-~--~                   ~---__|,--~'                  ~~----_____-~'   `~----~~
""".encode())
pr(b"What is the flag? ")
read()
a("popr 1")

for n in b"ictf{babyvm_sUccessfULly_craCKEd_ee938a5954da916add9bae5f1ebc458561e231134ae5ea06}"[::-1]:
  cmp(n)

pr(b"You win!\n")
a("ex")
for n in range(0x10000):
  a("nop")
pr(b"You lose!\n")
a("ex")
for n in range(0x1000):
  a("nop")

open("asm", "w").write(o)
os.system("python3 compile.py")
