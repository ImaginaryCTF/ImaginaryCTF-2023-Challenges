! Copyright (C) 2023 Robin Jadoul.
! See https://factorcode.org/license.txt for BSD license.
USING: command-line io kernel math math.bits math.functions math.matrices namespaces sequences vectors ;
IN: ictf.unfactored

: add ( a b -- c ) [ xor ] 2map ; inline

: shiftv ( b -- b ) 7 cut swap V{ } glue ; inline

: mulx ( v -- v )
    dup last
    [ shiftv V{ f f t t t f f f } add ]
    [ shiftv ]
    if ;

: b2i ( b -- i ) [ 1 ] [ 0 ] if ; inline

: v2a ( v -- a ) 8 <identity-matrix> [ 1 swap index over swap [ mulx ] times ] column-map nip ;

: n2v ( n -- v ) 256 mod 8 <bits> >vector ; inline

: n2a ( n -- a ) n2v v2a ; inline

: a2n ( a -- n ) 0 swap col 8 <iota> [ 2 swap ^ ] map [ swap b2i * ] 2map sum ;

: s2va ( s -- va ) >vector [ n2a ] map ;

: m** ( m m -- m ) [ b2i ] matrix-map swap [ b2i ] matrix-map mdot [ 2 mod 1 = ] matrix-map ;

: m++ ( m m -- m ) [ b2i ] matrix-map swap [ b2i ] matrix-map m+ [ 2 mod 1 = ] matrix-map ;

: eval ( a va -- a ) over swap [ -rot over m** rot over m** ] map 8 8 f <matrix> [ m++ ] reduce 2nip ;

: evals ( v -- w ) 256 <iota> >vector [ n2a over eval ] map nip ;

: checkvals ( -- v ) V{ 0 103 11 51 195 121 161 186 194 29 213 25 75 174 52 124 127 81 22 188 153 244 187 70 156 231 231 138 113 146 128 171 134 16 210 227 27 246 17 112 231 131 235 166 35 252 126 79 85 90 209 39 131 136 200 206 30 35 196 210 129 101 28 65 137 220 82 245 150 28 169 75 206 6 250 177 192 205 149 223 147 124 226 131 79 224 121 224 191 73 185 225 54 174 234 176 171 54 160 2 198 18 17 213 218 55 234 254 103 127 94 98 52 67 44 123 113 191 172 122 137 126 223 29 57 222 32 178 253 238 101 38 194 43 62 105 246 176 45 239 25 243 247 118 186 69 203 129 220 133 225 212 10 5 34 5 143 23 18 240 8 70 147 162 162 25 236 126 160 169 166 251 168 146 180 33 103 11 246 188 73 144 54 157 59 44 107 186 217 251 71 208 72 144 235 236 163 18 11 23 73 111 93 165 84 24 241 14 52 42 136 8 186 221 176 196 137 231 90 109 229 158 74 112 118 151 247 16 152 37 237 252 78 38 86 179 120 94 238 92 122 21 84 38 181 4 200 4 164 12 104 18 202 224 24 185 } ;

: checks ( v -- ? ) checkvals [ swap a2n = ] 2all? ;

: report ( ? -- ) [ "Correct" ] [ "Incorrect" ] if print ;

: main ( s -- ) dup s2va evals checks swap length 45 = and report ; inline

: main-run ( -- ) command-line get first main ;

MAIN: main-run
