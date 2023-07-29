from pwn import *
from Crypto.Util.number import *

core = Corefile('./core')

# struct with public/private keys at 0x00555555df95b8
n = bytes_to_long(core.read(0x00555555d1a440, 4096//8)[::-1])
e = 65537 # guessed
d = bytes_to_long(core.read(0x00555555dfb9b0, 4096//8)[::-1])

c = bytes_to_long(open("flag.enc", "rb").read())
print(long_to_bytes(pow(c,d,n)))
