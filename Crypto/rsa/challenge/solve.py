from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

key = RSA.importKey(open('private.pem', "rb").read())
flag = bytes_to_long(open("flag.enc", "rb").read())

print(long_to_bytes(pow(flag, key.d, key.n)))
