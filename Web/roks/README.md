# roks
**Category:** Web
**Difficulty:** Easy
**Author:** FIREPONY57

## Description

My rock enthusiast friend made a website to show off some of his pictures. Could you do something with it?

## Distribution

- source code with docker
- link

## Solution

- `index.php` is vulnerable to a directory transversal attack.
- Using url encoding to bypass the filter, we can use a payload such as `%25252E%25252E%25252F%25252E%25252E%25252F%25252E%25252E%25252F%25252E%25252E%25252F%25252E%25252E%25252F%25252E%25252E%25252F%25252E%25252E%25252Fflag%25252Epng` to grab the flag.

