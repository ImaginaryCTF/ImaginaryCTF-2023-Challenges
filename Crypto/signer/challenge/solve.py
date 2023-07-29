from pwn import *
from binascii import crc32
import os

#conn = process(["python3", "main.py"])
conn = remote("34.34.37.157", 1337)

conn.recvuntil(b"n = ")
n = int(conn.recvuntil(b"-").replace(b"\n", b"")[:-1])
target = crc32(b"give me the flag!!!")

t1 = target // 3
t2 = 3

# ./crchack dummy 3 | xxd
c1 = b'aaa2u<+'
# ./crchack dummy 0x4662352f | xxd
c2 = bytes.fromhex('6161 6161 6161 6161 6161 3344 470d')

conn.sendline(b'1')
conn.sendline(c1)
conn.recvuntil(b'Signature: ')
s1 = int(conn.recvline())

conn.sendline(b'1')
conn.sendline(c2)
conn.recvuntil(b'Signature: ')
s2 = int(conn.recvline())

conn.sendline(b'2')
conn.sendline(str((s1*s2)%n).encode())

conn.interactive()
