from sage.all import GF, matrix, vector
from operator import lshift, rshift
from random import setstate, getrandbits
from tqdm import trange
from pwn import process, context, remote

######## These 2 functions were shamelessly stolen from StealthyDev

def unxorshift(x, operator, shift, mask=0xFFFFFFFF):
    res = x
    for _ in range(32):
        res = x ^ (operator(res, shift) & mask)
    return res

def untemper(random_int):
    random_int = unxorshift(random_int, rshift, 18)
    random_int = unxorshift(random_int, lshift, 15, 0xefc60000)
    random_int = unxorshift(random_int, lshift,  7, 0x9d2c5680)
    random_int = unxorshift(random_int, rshift, 11)
    return random_int

###################################################################

def guess(bet, cards):
    io.sendlineafter(b'> ', b'play')
    io.sendlineafter(b': ', str(bet).encode())
    io.sendlineafter(b': ', ' '.join(DECK[int(c)] for c in cards).encode())

    raw   = io.recvline(False).decode()
    hand  = raw.split(': ')[1].split()
    total = raw.split('d ')[1].split()[0]
    return [*map(DECK.index, hand)], int(total)

def balance():
    io.recvuntil(b'balance: ')
    return int(io.recvline(False))

DECK = "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮"
n = 10

#io = process(['pyenv', 'exec', 'python3', './main.py'])
io = remote("34.34.17.46", 1337)
context.log_level = 'debug'

hands = []
col = [set(range(13)) for _ in range(n)]
M = []
i = 0
while i < n:
    hand, total = guess(1, i*[0] + [1] + (n-i-1)*[0])
    hands.append(hand)

    if total == 0:
        for r, c in zip(col, hand):
            r.discard(c)

        if all(len(r) == 1 for r in col):
            M.append([c for r in col for c in r])
            col = [set(range(13)) for _ in range(n)]
            i += 1
            print('i =', i)

print('M =', M)
print(f"Collected {len(hands)} hands")

F = GF(13)
M = matrix(F, M).T
f = M.charpoly()
L = f.splitting_field('z')
J, P = M.jordan_form(L, transformation=True)

print('Scanning matrix...')
print('order:', o := M.multiplicative_order(), f'({o.nbits()} bits)')
if o.nbits() < 32:
    print("Not enough bits!")
    exit()

for x in [n] + J.subdivisions()[0]:
    λ = J[x-1,x-1]
    print('λ ord:', n := λ.multiplicative_order(), f'({n.nbits()} bits)')
    if n == o:
        break
else:
    print("No eigenvalue was good enough!")
    exit()

print('Retrieving state...')
Q  = P**-1
hs = [(Q*vector(F, h))[x-1] for h in hands]

state = [
    int((hs[i+1]/hs[i]).log(λ))
    for i in trange(len(hs) - 1)
]

for i, s in enumerate(state):
    assert λ**s * hs[i] == hs[i+1]
    assert M**s * vector(F, hands[i]) == vector(F, hands[i+1])

setstate((3, tuple([*map(untemper, state[:624]), 624]), None))
for i in range(624, len(state)):
    assert state[i] == getrandbits(32)


context.log_level = 'debug'

cards = vector(F, hands[-1])
while (money := balance()) < 1_000_000_000:
    cards = M**getrandbits(32) * cards
    hand  = guess(money, M**-1 * cards)

io.sendlineafter(b'> ', b'buy flag')
io.interactive()
