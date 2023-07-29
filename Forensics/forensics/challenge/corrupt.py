from pwn import *
from os import urandom

f = open("raw.pcap", "rb").read()
out = b""
ptr = 0

def get(n, new=None):
  global ptr, out
  s = ptr
  ptr += n
  if new == None:
    out += f[s:s+n]
  else:
    assert len(new) == n
    out += new
  return f[s:s+n]

# pcap header
magic = get(4, urandom(4))
major = get(2)
minor = get(2)
reserved1 = get(4, urandom(4))
reserved2 = get(4, urandom(4))
snaplen = get(4)
flags = get(2)
linktype = get(2)

while ptr < len(f):
  timestamp_sec = get(4)
  timestamp_micro = get(4)
  captured_len = u32(get(4, urandom(4)))
  orig_len = u32(get(4))
  data = get(captured_len)
  print(captured_len)

open("forensics.pcap", "wb").write(out)
