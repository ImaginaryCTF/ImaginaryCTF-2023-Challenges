#!/usr/bin/env python3

# ~~stolen~~ borrowed from https://github.com/orsinium-labs/python-lambda-calculus
from lambda_calc import * 

from inspect import getsource
import regex

# https://codegolf.stackexchange.com/questions/250596/remove-redundant-parentheses
remove_parens = lambda s,p=0:s==p and s or remove_parens(regex.sub('(\(|^)\K(\((((?2)|[^()])*)\))(?=\)|$)',r'\3',s),s)

LISTEQ = Y(lambda f: lambda lsta: lambda lstb: EMPTY(lsta)
    (lambda _: TRUE)
    (lambda _: AND(EQ(HEAD(lsta))(HEAD(lstb)))(f(TAIL(lsta))(TAIL(lstb))))
    (TRUE)
)

ENC = Y(lambda f: (lambda n: (
    (INC(f(n-1))) if n else (ZERO)
)))

TOLIST = Y(lambda f: (lambda lst: (
    (PREPEND(f(lst[1:]))(ENC(lst[0]))) if len(lst) else (LIST())
)))

flag = b'ictf{d0_sh33p_b@@@?}'

MYLIST = "LIST()"

nmap = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN']

for char in flag[::-1]:
    num = f"ADD(MUL(SIXTEEN())({nmap[char//16]}()))({nmap[char%16]}())"
    MYLIST = f"PREPEND({MYLIST})({num})"

# MAP(lambda x: print(x(lambda y:y+1)(0)))(eval(MYLIST))

lambs = [i for i in globals() if i.isupper()]
my_code = lambda: (LISTEQ(MYLIST)(TOLIST(input(">>> ").encode( ))))

def src(f):
    if f == MYLIST:
        return MYLIST
    ret = getsource(f)
    # print(ret)
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
s = obsfucate(s)
out = remove_parens(f'print({s}("Well done!")("Try again..."))')
f = open("sheepish.py", "w")
f.write(out)
final = eval(out)
