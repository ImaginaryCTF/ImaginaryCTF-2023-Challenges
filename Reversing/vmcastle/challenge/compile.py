from pwn import *
import random

lookup = {'popr': 42, 'pushr': 43, 'pushi': 44, 'add': 45, 'sub': 46, 'mul': 47, 'idiv': 48, 'mod': 49, 'jmp': 50, 'jmpc': 51, 'cmp': 52, 'pr': 53, 'in': 54, 'shs': 55, 'ads': 56, 'ex': 57}
for n in lookup.keys():
  lookup[n] += 60
lookup['nop'] = 0

p = open("asm").read()
prog = []

for n in p.strip().split("\n"):
  if (len(n) == 0 or n[0] == '#'):
    continue
  if n.split()[0] == "nop":
    prog.append(random.randint(0,101)) # random nops for obfuscation
  else:
    prog.append(lookup[n.split()[0]])
  if n.split()[0] in ["popr", "pushr", "jmp", "pr", "in"]:
    prog.append(random.randint(0,63)*4 + int(n.split()[1], 0))
  elif n.split()[0] in ["shs", "ads"]:
    prog.append(random.randint(0,127)*2 +int(n.split()[1], 0))
  else:
    try:
      prog.append(int(n.split()[1], 0))
    except:
      prog.append(random.randint(0,255))

out = b""
for n in prog:
  if n < 0:
    out += (p8(n, signed=True))
  else:
    out += (p8(n))
open("out", "wb").write(out)
os.system("./vm out")
