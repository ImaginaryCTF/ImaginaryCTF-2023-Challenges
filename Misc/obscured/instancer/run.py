import os
import random
import string
import secrets
import hashlib
from time import time

# credit: https://github.com/balsn/proof-of-work/blob/master/nc_powser.py
class NcPowser:
    def __init__(self, difficulty=22, prefix_length=16):
        self.difficulty = difficulty
        self.prefix_length = prefix_length

    def get_challenge(self):
        return secrets.token_urlsafe(self.prefix_length)[:self.prefix_length].replace('-', 'b').replace('_', 'a')

    def verify_hash(self, prefix, answer):
        h = hashlib.sha256()
        h.update((prefix + answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.startswith('0' * self.difficulty)

name = "".join([random.choice(string.ascii_lowercase) for n in range(10)])
port = random.randint(40000, 50000)

powser = NcPowser()
powser.difficulty = 28
prefix = powser.get_challenge()
print("[*] Proof of work (https://balsn.tw/proof-of-work/):")
print("[*] Note: This may take a long time! The POW is here to help our infra stay alive.")
print(f"[*] sha256({prefix} + ???) == {'0'*powser.difficulty}({powser.difficulty})")
print(f"[*] Fast solver: https://github.com/RobinJadoul/proof-of-work/blob/faster-go/solver/go.go")
print(f"[*] $ ./solver {prefix} {powser.difficulty}")
hash = input("??? = ")
if not powser.verify_hash(prefix, hash):
  print("[*] Proof of work failed!")
  exit()

ip = os.popen("curl ifconfig.me 2>/dev/null").read()

print("[*] Starting challenge instance...")
os.system(f"docker run -dit --tmpfs /tmp --tmpfs /run -v /sys/fs/cgroup:/sys/fs/cgroup --cgroupns=host --name {name} -p {port}:22 --memory='75m' -e PASSWORD={name} --network no-internet obscured")
open("/root/instancer/instances", "a").write(f" {name}")
print("---------------------------------")
print("[*] Instance information:")
print(f"[*] ssh user@{ip} -p {port}")
print(f"[*] password: {name}")
print("---------------------------------")
print("[*] Note: All instances will be reset every 15 minutes.")
