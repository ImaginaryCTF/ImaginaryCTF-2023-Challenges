# crypto
**Category:** Forensics
**Difficulty:** Medium
**Author:** Eth007

## Description

Yes, my python program crashed. But I made sure to scrub all the sensitive details out of the coredump!

## Distribution

- `crypto.zip`

## Solution

- poke around in GDB around the scrubbed plaintext private key - near it is a struct with pointers to `n` and `d`
- solve.py
