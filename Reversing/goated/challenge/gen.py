#!/usr/bin/env python3

# ~~stolen~~ borrowed from https://github.com/orsinium-labs/python-lambda-calculus
from lambda_calc import * 

from inspect import getsource
import regex

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def bdec(b):
    out = ''
    while EMPTY(b)(False)(True):
        out += HEAD(b)('1')('0')
        b = TAIL(b)
    if out == '':
        return "bad"
    print(out)
    return int(out[::-1], 2)

# https://codegolf.stackexchange.com/questions/250596/remove-redundant-parentheses
remove_parens = lambda s,p=0:s==p and s or remove_parens(regex.sub('(\(|^)\K(\((((?2)|[^()])*)\))(?=\)|$)',r'\3',s),s)

LISTEQ = Y(lambda f: lambda lsta: lambda lstb: EMPTY(lsta)
    (lambda _: TRUE)
    (lambda _: AND(EQ(HEAD(lsta))(HEAD(lstb)))(f(TAIL(lsta))(TAIL(lstb))))
    (TRUE)
)

BLISTEQ = Y(lambda f: lambda lsta: lambda lstb: EMPTY(lsta)
    (lambda _: TRUE)
    (lambda _: AND(XNOR(HEAD(lsta))(HEAD(lstb))) (f(TAIL(lsta))(TAIL(lstb))))
    (TRUE)
)

ENC = Y(lambda f: (lambda n: (
    (INC(f(n-1))) if n else (ZERO())
)))

TOLIST = Y(lambda f: (lambda lst: (
    (PREPEND(f(lst[1:]))(ENC(lst[0]))) if len(lst) else (LIST())
)))

ZADD = Y(lambda f: (lambda b: lambda n: ISZERO(n)
    (lambda _: b)
    (lambda _: f(APPEND(b)(ZERO()))(DEC(n)))
    (TRUE)
))

ZPAD = lambda b: lambda n: ZADD(b)(SUB(n)(LENGTH(b)))

BENC = Y(lambda f: (lambda n: (
    (PREPEND(f(n>>1)) (NOT(ISZERO(ENC(n%2))) )) if n else (LIST())
)))

CONCAT = Y(lambda f: (lambda lsta: lambda lstb: EMPTY(lsta)
    (lambda _: lstb)
    (lambda _: PREPEND(f(TAIL(lsta))(lstb))(HEAD(lsta)))
    (TRUE)
))

TOBLIST = Y(lambda f: (lambda lst: (
    (CONCAT(f(lst[1:]))(ZPAD(BENC(lst[0]))(EIGHT()))) if len(lst) else (LIST())
)))

BNEG = Y(lambda f: (lambda b: EMPTY(b)
    (lambda _: LIST())
    (lambda _: PREPEND(f(TAIL(b)))(NOT(HEAD(b))))
    (TRUE)
))

BAR = lambda a: lambda b: lambda c: XOR(a)(XOR(b)(c))

# BAC = lambda a: lambda b: lambda c: GTE(ADD(ADD(CAST(a))(CAST(b)))(CAST(c)))(TWO())
BAC = lambda a: lambda b: lambda c: OR(AND(XOR(a)(b))(c))(AND(a)(b))


BADDHELP = Y(lambda f: (lambda a: lambda b: lambda c: EMPTY(a)
    (lambda _: LIST())
    (lambda _: PREPEND(f(TAIL(a))(TAIL(b))( BAC(HEAD(a))(HEAD(b))(c) ))( BAR(HEAD(a))(HEAD(b))(c) ))
    (TRUE)
))

BADD = lambda a: lambda b: BADDHELP(ZPAD(a)(LENGTH(b)))(ZPAD(b)(LENGTH(a)))(FALSE)

BSUB = lambda a: lambda b: BADDHELP(a)(BNEG(b))(TRUE)

BISNEG = Y(lambda f: (lambda a: EMPTY(TAIL(a))
    (lambda _: HEAD(a))
    (lambda _: f(TAIL(a)))
    (TRUE)
))

BGT = lambda a: lambda b: BISNEG(BSUB(b)(a))

BMODBAD = Y(lambda f: (lambda p: lambda q: BGT(q)(p)
    (lambda _: p)
    (lambda _: f(BSUB(p)(q)) (q))
    (TRUE)
))

BSUBGT = lambda a: lambda b: ((BGT(a)(b))
    (BSUB(a)(b))
    (a)
)

import dis
BMODHELP = Y(lambda f: (lambda n: lambda d: lambda r: EMPTY(n)
    (lambda _: r)
    (lambda _: 
        f(TAIL(n))(d)( BSUBGT( PREPEND(r)(HEAD(n)) )(d) )
    )
    (TRUE)
))

BMOD = lambda n: lambda d: [TAKE(LENGTH(n)) (BMODHELP(REVERSE(n)) (d) (ZADD(LIST())(LENGTH(n)))), print(bdec(n))][0]

BMULHELP = lambda a: lambda b:(b
    (a)
    (ZPAD(LIST())(LENGTH(a)))
)

BMUL = Y(lambda f: (lambda a: lambda b: EMPTY(b)
    (lambda _: LIST())
    (lambda _: BADD(BMULHELP(a)(HEAD(b)))( PREPEND(f(a)(TAIL(b)))(FALSE) ) )
    (TRUE)
))

BMM = lambda a: lambda b: lambda n: BMOD(BMUL(a)(b))(n)

POWMODHELP = Y(lambda f: (lambda b: lambda e: lambda n: lambda r: EMPTY(e)
    (lambda _: r)
    (lambda _:
        HEAD(e)
        ( f(BMUL(b)(b))(TAIL(e))(n)(BMUL(b)(r)) )
        ( f(BMUL(b)(b))(TAIL(e))(n)(r) )
    )
    (TRUE)
))

POWMODFAKE = lambda b: lambda e: lambda n: POWMODHELP(b)(e)(n)(ZPAD(TOBLIST(b'\x01'))(LENGTH(n)))

POWMOD = lambda b: lambda e: lambda n: BMOD(POWMODFAKE(b)(e)(n))(n)

inc = lambda x:x+1
# z = TOBLIST(b'abc')
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BNEG(TOBLIST(b'abc'))
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BSUB(TOBLIST(b'abc')) (TOBLIST(b'abe')) 
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BSUB(TOBLIST(b'abc')) (TOBLIST(b'add')) 
# print(BISNEG(z)(True)(False))

# z = BGT(TOBLIST(b'abc')) (TOBLIST(b'abb')) 
# print((z)(True)(False))

# z = BSUBGT(TOBLIST(b'abc')) (TOBLIST(b'abb')) 
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BMOD(TOBLIST(b'\x1f\xff')) (TOBLIST(b'\x00\x04'))
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BMOD(TOBLIST(b'~123456789abcdef0123456789abcdef')) (TOBLIST(b'0123456789abcdef0123456789abcdef'))
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = BMUL(TOBLIST(b'\x00\x00\xff')) (TOBLIST(b'\x00\x00\xff'))
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

# z = POWMOD(TOBLIST(b'\x00\x00\x00\x00\x01\xff')) (PREPEND((PREPEND(LIST())(TRUE)))(TRUE)) (TOBLIST(b'\x00\x00\x00\x0f\x00\x00'))
# while EMPTY(z)(False)(True):
#     print(HEAD(z)(ONE())(ZERO())(inc)(0), end='')
#     z = TAIL(z)
# print()

bits = 8

# p = getPrime(bits)
# q = getPrime(bits)
# m = bytes_to_long(b'a')
# n = p*q
# c = pow(m, 3, n)
# cb = (ZPAD(TOBLIST(long_to_bytes(c)))(ENC((bits+1)*3)))
# nb = (ZPAD(TOBLIST(long_to_bytes(n)))(ENC((bits+1)*3)))
# mb = (ZPAD(TOBLIST(long_to_bytes(m)))(ENC((bits+1)*3)))


BTHREE = lambda: PREPEND((PREPEND(LIST())(TRUE)))(TRUE)
# right = POWMOD(mb)(BTHREE)(nb)
# out = BLISTEQ(cb)(right)

# print(bdec(cb))
# print(bdec(right))

# dis.dis(out)
# print(out(True)(False))

# while EMPTY(cb)(False)(True):
#     print(HEAD(cb)(1)(0), end='')
#     cb = TAIL(cb)
# print()

# while EMPTY(right)(False)(True):
#     print(HEAD(right)(1)(0), end='')
#     right = TAIL(right)
# print()

# exit()

SEVENTYFIVE = lambda: MUL(MUL(FIVE())(FIVE()))(THREE())
from random import randint
flag = b'G()@+3c|!~'
x = bytes_to_long(flag)
print(x)
print(bdec(TOBLIST(flag)))
a = randint(0, x)
b = randint(0, x)
c = x * a + b

ALIST = "LIST()"
BLIST = "LIST()"
CLIST = "LIST()"

print(a)
for bit in bin(a)[2:]:
    ALIST = f"PREPEND({ALIST})({'TRUE' if bit == '1' else 'FALSE'})"
print(bdec(eval(ALIST)))
print()
print(b)
for bit in bin(b)[2:]:
    BLIST = f"PREPEND({BLIST})({'TRUE' if bit == '1' else 'FALSE'})"
print(bdec(eval(BLIST)))
print()
print(c)
for bit in bin(c)[2:]:
    CLIST = f"PREPEND({CLIST})({'TRUE' if bit == '1' else 'FALSE'})"
print(bdec(eval(CLIST)))


lambs = [i for i in globals() if i.isupper()]

# MYLIST is c?
# LISTEQ(MYLIST)(POWMOD(TOBLIST(input))(3)(N))
# my_code = lambda: (BLISTEQ
#     (ZPAD(eval(CLIST))(SEVENTYFIVE()))
#     (POWMOD
#         (ZPAD(TOBLIST(input(">>> ").encode( )))(SEVENTYFIVE()))
#         (BTHREE())
#         (ZPAD(eval(NLIST))(SEVENTYFIVE()))
#     )
# )

my_code = lambda: (BLISTEQ
    (CLIST)
    (BADD
        (BMUL
            (TOBLIST(input(">>> ").encode( )))
            (ALIST)
        )
        (BLIST)
    )
)

# print(my_code()(True)(False))
# exit()  

def src(f):
    if f in [ALIST, BLIST, CLIST]:
        return f
    ret = getsource(f)
    ret = ret.split(" = ")[-1]
    ret = ret.replace("  ", "")
    ret = ret.replace("\n", "")
    return ret

def stringify(f):
    fs = src(f)
    while any([(i in fs) for i in lambs]):
        for lamb in lambs:
            if lamb not in fs:
                continue
            fs = regex.sub(
                r"([^A-Z]|^)" + lamb + r"([^A-Z]|$)",
                "\\1(" + src(globals()[lamb]) + ")\\2",
                fs
            )
    return remove_parens(fs)

def obsfucate(s):
    varnames = list(set(regex.findall("[a-z]+", s)))
    reserved = ["input", "encode", "else", "if", "len", "lambda"]
    for i in reserved:
        varnames.remove(i)
    for i, v in enumerate(varnames):
        for _ in range(2):
            s = regex.sub(
                r"(\W)" + v + r"(\W)",
                "\\1" + "_"*(i+1) + "\\2",
                s
            )
    return s

s = stringify(my_code)
s = s.replace("lambda: ", "")
s = s.replace("()", "")
s = s.replace("( )", "()")
s = s.replace(": ", ":")
# print(s)
s = obsfucate(s)
out = remove_parens(f'print({s}("Well done!")("Try again..."))')
f = open("goated.py", "w")
f.write(out)
final = eval(out)
print(final)
