from Crypto.Util.number import long_to_bytes, bytes_to_long
from sage.all import matrix, QQ
from hashlib import sha1
from pwn import *
import random
import string
import ecdsa

context.binary = elf = ELF("./elliptic")
#conn = elf.process()
conn = remote("34.91.101.142", 1337)
#context.log_level = 'debug'
#gdb.attach(conn)

def random_string():
  return bytes([ord(random.choice(string.ascii_letters)) for n in range(20)])

def convert_number_in(h): # account for little endian signatures
  return bytes_to_long(bytes.fromhex(h)[::-1])

def convert_number_out(n): # account for little endian signatures
  n = hex(n)[2:]
  if len(n) % 2 == 1:
    n = '0' + n
  return bytes.fromhex(n)[::-1].hex().upper().encode()

def shash(s):
  return bytes_to_long(sha1(s).digest()[:16][::-1])

def get_signature():
  conn.sendlineafter(b">", b"1")
  conn.sendlineafter(b":\n", b"asdf")
  conn.recvuntil(b"r = ")
  r = convert_number_in(conn.recvline().strip().decode())
  conn.recvuntil(b"s = ")
  s = convert_number_in(conn.recvline().strip().decode())
  return r, s

def get_corrupted_signature(r, s):
  msg = random_string()
  conn.sendlineafter(b">", b"2")
  # make a valid signature using (r,-s)
  conn.sendlineafter(b"r = ", convert_number_out(r))
  conn.sendlineafter(b"s = ", convert_number_out(ecdsa.SECP128r1.order-s))
  conn.sendlineafter(b":\n", b"asdf")
  conn.sendlineafter(b":\n", msg)
  conn.recvuntil(b"r = ")
  cr = convert_number_in(conn.recvline().strip().decode())
  conn.recvuntil(b"s = ")
  cs = convert_number_in(conn.recvline().strip().decode())
  return cr, cs, msg

def ecdsa_sign(val, secret_exponent):
  curve = ecdsa.SECP128r1
  n = curve.order
  G = curve.generator
  k = 1337 # lol
  p1 = k * G
  r = p1.x()
  if r == 0: raise RuntimeError("amazingly unlucky random number r")
  s = ( ecdsa.numbertheory.inverse_mod( k, n ) * ( val + ( secret_exponent * r ) % n ) ) % n
  if s == 0: raise RuntimeError("amazingly unlucky random number s")
  return r, s

def recover_sk(hashes, sigs):
  q = ecdsa.SECP128r1.order # curve order (secp128r1 parameter)
  X = 1 << 16*8 # bound on secret key
  N = 1 << 14*8 # bound on nonces (2 ms bytes are 0)

  n = len(hashes)

  # -s*k + r*x + h = 0
  M = matrix(QQ, [
      [*hashes],
      [r for r, _ in sigs],
      *[
          [0]*i + [s] + [0]*(n-i-1)
          for i, (_, s) in enumerate(sigs)
      ],
  ])                                                                  \
  .augment(matrix.identity(QQ, n+2))                                  \
  .stack(matrix.diagonal(QQ, [q]*n).augment(matrix.zero(QQ, n, n+2))) \
  .dense_matrix()
  # weights
  W = matrix.diagonal([1]*n + [1, 1/QQ(X)] + [1/QQ(N)]*n)

  print('LLL...')
  L = (M*W).LLL()/W
  print('LLL done!')

  for row in L:
    if row[:n] == 0 and abs(row[n]) == 1:
      if (int(row[n+1]*row[n]) < 0):
        return q + int(row[n+1]*row[n])
      else:
        return int(row[n+1]*row[n]) # row[n+1] is the secret key, up to sign

  print("No luck")

hashes = []
sigs = []
for _ in range(9):
  r, s = get_signature()
  cr, cs, msg = get_corrupted_signature(r, s)
  print(cr, cs, msg)
  hashes.append(shash((msg+b'\n').ljust(64, b'\0')))
  sigs.append([cr,cs])

secret = recover_sk(hashes, sigs)

conn.sendlineafter(b'>', b'3')
conn.recvuntil(b"magic = ")
magic = convert_number_in(conn.recvline().strip().decode())
r, s = ecdsa_sign(magic, secret)
conn.sendlineafter(b"r = ", convert_number_out(r))
conn.sendlineafter(b"s = ", convert_number_out(s))

conn.stream()
