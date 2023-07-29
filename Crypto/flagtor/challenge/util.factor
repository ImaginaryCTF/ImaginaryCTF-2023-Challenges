! Copyright (C) 2023 Robin Jadoul.
! See https://factorcode.org/license.txt for BSD license.
USING: command-line io io.encodings.utf8 io.files kernel math math.matrices math.parser namespaces prettyprint random sequences vectors ;
IN: ictf.flagtor_util

: flag-length ( -- n ) 41 ;

: with-seed ( ... n quot -- ... ) swap random-generator get swap seed-random swap with-random ; inline
: 2vec ( ... a b -- ... v ) swap V{ } clone -rot pick push over push ;
: into-matrix ( v -- m ) dup length dup [ 2drop dup random random-32 -24 shift 2vec ] <matrix-by-indices> nip ;

: main ( -- ) command-line get first string>number [ flag-length 1 + <iota> >vector into-matrix . ] with-seed ;

MAIN: main
