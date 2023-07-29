# sheepish
**Category:** Reversing
**Difficulty:** Medium
**Author:** puzzler7

## Description

Mary had a flagchecker,
its fleece was white as snow.

## Distribution

- `sheepish.py`

## Solution

This challenge uses lambda calculus to compare the user input to a hardcoded list.

We can immediately see from the end of the program that it is using [Church booleans](https://en.wikipedia.org/wiki/Church_encoding#Church_Booleans) - that is to say, it returns a lambda function that will return the first thing (`Well done!`) if true, and the second thing (`Try again...`) if false. The program using Church encodings for other datatypes (lists and numbers).

Entering a short input will cause the program to crash - the shortest input that will run the program is of length 20, so we can assume the flag is length 20.

After removing the print at the beginning and the strings at the end, we can see that the function is composed of three parts at the highest level of parentheses - this implies it is a function with two arguments. The first part is the function that takes in these two arguments, the second is a massive blob of lambdas that hardcodes the flag value, and the third takes the user input and converts it to a list.

Iterating through the list and decoding its Church numerals to numbers yields the flag.
