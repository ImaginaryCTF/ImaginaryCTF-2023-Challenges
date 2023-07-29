#!/usr/bin/env python3

import urllib.request
import subprocess
import os
import uuid

fname = str(uuid.uuid4())

url = input("Give me the URL to your exploit executable (press enter to skip): ")
if url == "":
    path = ""
else:
    path = f"/dev/shm/{fname}"

    # Downloading the user's exploit executable.
    try:
        assert urllib.parse.urlparse(url).scheme in ["http", "https"]
        with urllib.request.urlopen(url) as f:
            exploit = f.read()
    except Exception:
        print("Some error occurred while downloading your exploit executable. Try again or contact support :(\n")
        exit(-1)
    else:
        # Saving the user's exploit executable to a tmp disk file.
        with open(path, "wb") as f:
            f.write(exploit)

try:
    subprocess.run(["./run.sh", path])
except Exception:
    print("Some error occurred while running qemu. Try again or contact support :(\n")

if path != "":
    os.unlink(path)
