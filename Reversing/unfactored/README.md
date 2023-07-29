# unfactored
**Category:** Reversing
**Difficulty:** Medium/Hard
**Author:** Robin_Jadoul

## Description

Something in the challenge is unfactored for sure, but does it really matter if everything else is factor?
Usage: `./ictf.unfactored <flag>`

## Distribution

- `ictf.unfactored`

## Solution

This is a challenge written in [factor](https://factorcode.org/), a stack-based language.
You can easily figure out the languages/runtime from the strings in the binary, and the VM can be inspected in source code form.
Upon finding the VM bytecode and reverse engineering it a bit, you can figure out that it performs 255 (+ 1 incorrect one) polynomial evaluations over GF(2^8) with defining polynomial x^8 + x^4 + x^3 + x^2 + 1 by translating everything to matrix form and evaluating the polynomials there.
Afterwards, it simply checks all computed values after converting back to integer representation of the field.
Extracting the checking values and interpolating it (e.g. with sagemath), we can get the flag from the recovered coefficients.
