#!usr/bin/env python3

# ~~stolen~~ borrowed from https://github.com/orsinium-labs/python-lambda-calculus

IDENTITY = lambda a: a
IF = IDENTITY

# boolean values
TRUE  = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

# base boolean operations
OR  = lambda a: lambda b: a(TRUE)(b)
AND = lambda a: lambda b: a(b)(FALSE)
NOT = lambda a: a(FALSE)(TRUE)

# additional boolean operations
XOR  = lambda a: lambda b: a(b(FALSE)(TRUE))(b(TRUE)(FALSE))
XNOR = lambda a: lambda b: NOT(XOR(a)(b))

# arithmetic
INC = lambda n: lambda a: lambda b: a(n(a)(b))
ADD = lambda a: lambda b: a(INC)(b)
MUL = lambda a: lambda b: lambda c: a(b(c))
DEC = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda _: x)(IDENTITY)
SUB = lambda a: lambda b: b(DEC)(a)
POW = lambda a: lambda b: b(a)
DIFF = lambda a: lambda b: ADD(SUB(a)(b))(SUB(b)(a))

# numbers
ZERO  = lambda: FALSE
ONE   = lambda: IDENTITY
TWO   = lambda: lambda a: lambda b: a(a(b))
THREE = lambda: lambda a: lambda b: a(a(a(b)))
FOUR  = lambda: INC(THREE())
FIVE  = lambda: ADD(TWO())(THREE())
SIX   = lambda: MUL(TWO())(THREE())
SEVEN = lambda: INC(SIX())
EIGHT = lambda: MUL(FOUR())(TWO())
NINE  = lambda: POW(THREE())(TWO())
TEN   = lambda: MUL(FIVE())(TWO())

ELEVEN = lambda: ADD(SEVEN())(FOUR())
TWELVE = lambda: MUL(POW(TWO())(TWO()))(THREE())
THIRTEEN = lambda: ADD(SIX())(SEVEN())
FOURTEEN = lambda: MUL(SEVEN())(TWO())
FIFTEEN = lambda: MUL(FIVE())(THREE())
SIXTEEN = lambda: POW(TWO())(FOUR())

# checks
ISZERO = lambda a: a(lambda _: FALSE)(TRUE)
GTE = lambda a: lambda b: ISZERO(SUB(b)(a))
LTE = lambda a: lambda b: ISZERO(SUB(a)(b))
GT  = lambda a: lambda b: ISZERO(SUB(INC(b))(a))
LT  = lambda a: lambda b: ISZERO(SUB(INC(a))(b))
EQ  = lambda a: lambda b: AND(GTE(a)(b))(LTE(a)(b))

# advanced arithmetic
MIN  = lambda a: lambda b: LTE(a)(b)(a)(b)
MAX  = lambda a: lambda b: GTE(a)(b)(a)(b)

# pair
CONS = lambda a: lambda b: lambda c: c(a)(b)
CAR  = lambda p: p(TRUE)
CDR  = lambda p: p(FALSE)

# The Billion Dollar Mistake
NULL   = lambda _: TRUE
ISNULL = lambda _: lambda _: FALSE

# combinators
I = IDENTITY
K = TRUE
S = lambda a: lambda b: lambda c: a(c)(b(c))
Y = lambda f: (
    (lambda x: f(lambda y: x(x)(y)))
    (lambda x: f(lambda y: x(x)(y)))
)

# made list a lambda here to cheese getsource
LIST = lambda: CONS(TRUE)(TRUE)
PREPEND = lambda xs: lambda x: CONS(FALSE)(CONS(x)(xs))
EMPTY = lambda xs: CAR(xs)
HEAD = lambda xs: CAR(CDR(xs))
TAIL = lambda xs: CDR(CDR(xs))
APPEND = Y(
    lambda f: lambda xs: lambda x: EMPTY(xs)
    (lambda _: PREPEND(xs)(x))
    (lambda _: CONS(FALSE)(CONS(HEAD(xs))(f(TAIL(xs))(x))))
    (TRUE)
)
REVERSE = Y(
    lambda f: lambda xs: EMPTY(xs)
    (lambda _: LIST())
    (lambda _: APPEND(f(TAIL(xs)))(HEAD(xs)))
    (TRUE)
)
# MAP(a)(xs): apply `a` function to every element in `xs` list.
# Return list of results for every element.
MAP = Y(
    lambda f: lambda a: lambda xs: EMPTY(xs)
    (lambda _: LIST())
    (lambda _: PREPEND(f(a)(TAIL(xs)))(a(HEAD(xs))))
    (TRUE)
)
RANGE = Y(
    lambda f: lambda a: lambda b: GTE(a)(b)
    (lambda _: LIST())
    (lambda _: PREPEND(f(INC(a))(b))(a))
    (TRUE)
)
# REDUCE(r)(l)(v):
# 1. Apply pass head of `l` and `v` into `r` and save result into `v`.
# 2. Do it for every element into lest from left to right.
# 3. Return `v` (accumulated value)
REDUCE = FOLD = Y(
    lambda f: lambda r: lambda l: lambda v: EMPTY(l)
    (lambda _: v)  # if list is empty, return accumulated value (v)
    # pass accumulated value (v) and head into reducer (r)
    # do reucing on tail of list (l) with a new accumulated value (v)
    (lambda _: f(r)(TAIL(l))(r(HEAD(l))(v)))
    (TRUE)
)
FILTER = lambda f: lambda l: (
    REDUCE
    (lambda x: lambda xs: f(x)(APPEND(xs)(x))(xs))
    (l)
    (LIST())
)
DROP = lambda n: lambda l: n(TAIL)(l)
TAKE = Y(lambda f: lambda n: lambda l: (
    OR(EMPTY(l))(ISZERO(n))
    (lambda _: LIST())
    (lambda _: (
        PREPEND(f(DEC(n))(TAIL(l)))
        (HEAD(l))
    ))
    (TRUE)
))
LENGTH = lambda l: REDUCE(lambda x: lambda n: INC(n))(l)(ZERO)
INDEX = Y(lambda f: lambda n: lambda l: (
    ISZERO(n)
    (lambda _: HEAD(l))
    (lambda _: f(DEC(n))(TAIL(l)))
    (TRUE)
))
ANY = Y(lambda f: lambda l: (
    EMPTY(l)
    (lambda _: FALSE)
    (lambda _: HEAD(l)(TRUE)(f(TAIL(l))))
    (TRUE)
))
ALL = Y(lambda f: lambda l: (
    EMPTY(l)
    (lambda _: TRUE)
    (lambda _: NOT(HEAD(l))(FALSE)(f(TAIL(l))))
    (TRUE)
))

DIV = lambda: Y(
    lambda f: lambda a: lambda b: LT(a)(b)
    (lambda _: ZERO)
    (lambda _: INC(f(SUB(a)(b))(b)))
    (ZERO)
)
MOD = lambda: Y(
    lambda f: lambda a: lambda b: LT(a)(b)[0]
    (lambda _: a)
    (lambda _: f(SUB(a)(b))(b))
    (ZERO)
)