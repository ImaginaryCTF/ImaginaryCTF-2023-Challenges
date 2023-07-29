# blank
**Category:** Web
**Difficulty:** Easy
**Author:** Eth007

## Description

I asked ChatGPT to make me a website. It refused to make it vulnerable so I added a little something to make it interesting. I might have forgotten something though...

## Distribution

- `blank_dist.zip`
- link

## Solution

- "Normal" SQLi payloads should fail becuase the database is blank (as can be seen from the lack of initialization in the code)
- The credentials `admin` and `" union select 1,1,1 from sqlite_master /*` will make the server think that this username/password pair returned an user, even though the database is really blank. 
