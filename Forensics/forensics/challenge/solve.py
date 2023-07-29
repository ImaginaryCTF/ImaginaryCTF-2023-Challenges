from pwn import *

f = open("forensics.pcap", "rb").read()
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

def set_prev(new):
  global out
  save = out[-4:]
  out = out[:-8]
  out += new
  out += save

# pcap header
magic = get(4, b"\xd4\xc3\xb2\xa1")
major = get(2)
minor = get(2)
reserved1 = get(4, b"\0\0\0\0")
reserved2 = get(4, b"\0\0\0\0")
snaplen = get(4)
flags = get(2)
linktype = get(2)

while ptr < len(f):
  timestamp_sec = get(4)
  timestamp_micro = get(4)
  captured_len = u32(get(4))
  orig_len = u32(get(4))
  set_prev(p32(orig_len))
  data = get(orig_len)
  print(captured_len)

open("solve.pcap", "wb").write(out)

