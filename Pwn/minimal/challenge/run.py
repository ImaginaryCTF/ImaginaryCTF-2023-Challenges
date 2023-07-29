#!/usr/bin/env python3

import time
import sys
from subprocess import Popen, PIPE, STDOUT

count = int(input("How many lines of input: "))
lines = []
for n in range(count):
  lines.append(bytes.fromhex(input("hex> ")))
#print(lines)

p = Popen(['./vuln'], stdin=PIPE, stdout=PIPE)
for line in lines:
  p.stdin.write(line)
while True:
  line = p.stdout.readline()
  if not line: break
