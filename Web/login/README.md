# login
**Category:** Web
**Difficulty:** Easy
**Author:** maple3142

## Description

A classic PHP login page, nothing special.

## Distribution

- link

## Solution

- Use union-based SQLi to login as admin to get the magic
- The fact that Bcrypt truncates the password to 72 characters can be used as an oracle to bruteforce the flag.
