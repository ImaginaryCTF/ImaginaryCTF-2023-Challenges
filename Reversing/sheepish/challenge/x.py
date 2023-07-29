#!/usr/bin/env python3

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


sheep = (
    open("sheepish.py").read().strip()
    .replace("print((", "").replace(')("Well done!")("Try again..."))','')
)
listeq, sheep = matching_paren(sheep)
flaglist, sheep = matching_paren(sheep)
userinput, sheep = matching_paren(sheep)

flaglist = eval(flaglist)

flag = []
head = lambda lst: lst(lambda a: lambda b: b)(lambda a: lambda b: a)
tail = lambda lst: lst(lambda a: lambda b: b)(lambda a: lambda b: b)
isempty = lambda lst: lst(lambda a: lambda b: a)(True)(False)
while not isempty(flaglist):
    flag.append(decode_num(head(flaglist)))
    flaglist = tail(flaglist)

print(bytes(flag))
