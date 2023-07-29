# scrambled
**Category:** Reversing
**Difficulty:** Easy
**Author:** cleverbear57

## Description

The flag is all jumbled up... or is it?

## Distribution

- `main`
- nc

## Solution

The encryption is its own inverse, so you can decrypt by putting the stored ciphertext back in and searching for `ictf` in GDB.
