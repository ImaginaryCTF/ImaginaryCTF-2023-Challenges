from pwn import process, xor
import os, pickle
DEBUG = False

def get_matrix(i):
    io = process(["../../../factor", "util.factor", str(i)])
    io.recvuntil(b"{")
    res = []
    for _ in range(MATLEN):
        res.append([])
        io.recvuntil(b"{")
        for _ in range(MATLEN):
            io.recvuntil(b"V{")
            res[-1].append(tuple(map(int, io.recvuntil(b"}", drop=True).decode().strip().split())))
        io.recvuntil(b"}")
    io.recvuntil(b"}")
    assert not (x := io.recvall().strip()), x
    return res

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

with open("out.txt") as f:
    data = f.read()

data = [list(map(int, x.split())) for x in "".join(data.splitlines())[2:].replace("}", "").split("{")]
ciphertext = data.pop(0)
DROPPED = 26
MATLEN = len(data) + DROPPED
if not os.path.exists("matrix.pkl"):
    matrix = sum((transpose(get_matrix(i)) for i in range(len(data))), start=[])
    with open("matrix.pkl", "wb") as f:
        pickle.dump(matrix, f)
else:
    with open("matrix.pkl", "rb") as f:
        matrix = pickle.load(f)


plain = b"ictf{" + b"\0" * (MATLEN - 1 - 6) + b"}"
assert len(plain) == len(ciphertext)
KNOWN_MASK = xor(plain, ciphertext)
INDEX = {}
RINDEX = {-1: None}
CONSTANTS = {MATLEN - 1: 1, MATLEN - 2: KNOWN_MASK[-1]} | {i: k for i, k in enumerate(KNOWN_MASK[:5])} 
def index_value(x, y, assert_exists = False):
    v = 1
    if x in CONSTANTS:
        v *= CONSTANTS[x]
        x = MATLEN - 1
    if y in CONSTANTS:
        v *= CONSTANTS[y]
        y = MATLEN - 1
    if x == y == MATLEN - 1:
        return None, v
    x, y = sorted([x, y])
    if (x, y) not in INDEX:
        assert not assert_exists, "Uhhmm"
        INDEX[(x, y)] = max(RINDEX) + 1
        RINDEX[INDEX[(x, y)]] = (x, y)
    return INDEX[(x, y)], v


def row_res(r):
    row = {}
    constant = 0
    for x, y in zip(r, range(MATLEN)):
        idx, v = index_value(x[0], y)
        v *= x[1]
        if idx is None:
            constant += v
        else:
            row[idx] = row.get(idx, 0) + v
    return (row, constant)

def matrix_row(r):
    return row_res(r)[0]

def sol_col(r):
    return row_res(r)[1]

def dict_to_row(r):
    res = [0 for _ in range(max(RINDEX) + 1)]
    for k, v in r.items():
        res[k] += v
    return res

rows = [matrix_row(r) for r in matrix]
print(f"{len(INDEX)} unknowns after linearization.")
M = Matrix(GF(257), [dict_to_row(r) for r in rows])
b = vector(GF(257), sum(data, start=[]))
print(M.right_kernel())

if DEBUG:
    REAL_MASK = xor(open("flag.txt", "rb").read().strip(), ciphertext)
    REAL_MASK += b"\x01"
    assert vector(GF(257), [sum(REAL_MASK[i] * REAL_MASK[j] * c for i, (j, c) in enumerate(r)) for r in matrix]) == b
    REAL_MASK = REAL_MASK[:-1]
    print("Assert success")

b -= vector(GF(257), [sol_col(r) for r in matrix])

solution = M \ b
def solget(i):
    for j in CONSTANTS:
        idx, v = index_value(i, j)
        if idx is None: return ZZ(GF(257)(v) / CONSTANTS[j])
        if idx < len(solution): return ZZ(GF(257)(solution[idx]) / CONSTANTS[j])

    idx, v = index_value(i, i, True)
    if idx is None: return ZZ(sqrt(v))
    if idx < len(solution): return ZZ(sqrt(solution[idx]))

print(xor(ciphertext, bytes(int(solget(i)) for i in range(MATLEN - 1))).decode())
