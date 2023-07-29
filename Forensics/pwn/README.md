# pwn
**Category:** Forensics
**Difficulty:** Medium
**Author:** Eth007

## Description

Someone got into my server. But at least I had proper logging in place! Can you figure out how they got in?

## Distribution

- `pwn.pcap`

## Solution

- one of the packets has the public IP of the server in it (from curl ifconfig.me)
- connect to the server on port 42067, you get the service
- reverse engineer the exploit (get libc from the unsorted bin address, or the system() address)
- exploit the service and get the flag
