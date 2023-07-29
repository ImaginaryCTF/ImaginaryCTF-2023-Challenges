from PIL import Image
import random

flag = [int(n) for n in bin(int(b"ictf{the_original_image_reveals_all_b1f9a293}".hex(), 16))[2:]]

im = Image.open("./original.png")
pixels = im.load()

for i in range(im.size[0]):
  for j in range(im.size[1]):
    if random.randint(0,50) == 1 and len(flag) > 0:
      r, g, b, a = pixels[i,j]
      pixels[i,j] = (r+flag.pop(0), g, b+1, a)

assert len(flag) == 0
im.save("chall.png")
