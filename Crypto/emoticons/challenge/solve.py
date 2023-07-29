text = open("out.txt").read()
sample = open("sample.txt").read()

sample = sample.encode().hex()

emojis = [n for n in list(set(text))]
emojis.sort(reverse=True, key=lambda x:text.count(x))

nibbles = [n for n in "0123456789abcdef"]
nibbles.sort(reverse=True, key=lambda x:sample.count(x))

for n in nibbles:
  print(n, sample.count(n))

for e, c in zip(emojis, nibbles):
  text = text.replace(e, c)

print(bytes.fromhex(text))

