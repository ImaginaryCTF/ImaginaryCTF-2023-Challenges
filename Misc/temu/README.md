# temu
**Category:** Misc
**Difficulty:** Easy-Medium
**Author:** puzzler7

## Description

Writing a terminal emulator is one of those things that's not-that-hard to get a proof of concept, but making a polished final product can be tricky. I know there's many a flaw in this one, but I tried to at least make it as pretty as possible

## Distribution

- temu.py
- socat connection as below:

```
socat FILE:`tty`,raw,echo=0 TCP:<ip address>:<port>
```

## Solution

We need to be logged in as alice to have access to the flag, but the only user who can cat files is eve.

There's a vulnerability in the syntax highlighting - the regex for the filepaths has a [ReDoS](https://www.regular-expressions.info/redos.html) in it. This can cause the processing of the commands to take longer, allowing up to queue up a cat command as eve, and stall its execution until we can login as alice.

The following input will yield the flag (add or subtract `/a`s to increase/decrease the delay)

```
login eve
cat /home/a/flag.txt /a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a
login alice
```
