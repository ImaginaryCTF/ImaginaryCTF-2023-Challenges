#!/usr/bin/env python3

from Crypto.Util.number import *

def matching_paren(s):
    if s[0] != '(':
        print("doesn't start w paren")
        exit()
    depth = 1
    i = 1
    while depth > 0:
        if s[i] == '(':
            depth += 1
        if s[i] == ')':
            depth -= 1
        i += 1
    return s[:i], s[i:]

def decode_num(n):
    return n(lambda x:x+1)(0)

head = lambda lst: lst(lambda a: lambda b: b)(lambda a: lambda b: a)
tail = lambda lst: lst(lambda a: lambda b: b)(lambda a: lambda b: b)
isempty = lambda lst: lst(lambda a: lambda b: a)(True)(False)

def bdec(b):
    out = ''
    while not isempty(b):
        out += head(b)('1')('0')
        b = tail(b)
    if out == '':
        return "bad"
    return int(out[::-1], 2)


goat = (
    open("goated.py").read().strip()
    .replace("print((", "").replace(')("Well done!")("Try again..."))','')
)
listeq, goat = matching_paren(goat)
c, goat = matching_paren(goat)
userinput, goat = matching_paren(goat)

userinput = userinput[1:-1]

add, userinput = matching_paren(userinput)
mulres, userinput = matching_paren(userinput)
b, userinput = matching_paren(userinput)

mulres = mulres[1:-1]

mul, mulres = matching_paren(mulres)
userinput, mulres = matching_paren(mulres)
a, mulres = matching_paren(mulres)

c = bdec(eval(c))
b = bdec(eval(b))
a = bdec(eval(a))

print(a, b, c)

x = (c - b)//a
print(long_to_bytes(x))


# print(bytes(flag))
