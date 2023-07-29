from PIL import Image
import exiftool

def add_metadata(image_path, field, value):
  with exiftool.ExifTool() as et:
    metadata = [f"-{field}={value}"]
    et.execute(*metadata, image_path)

image = Image.new('RGBA', (690, 420), (255, 255, 255))

image.putpixel((412, 309), (52, 146, 235, 123))
image.putpixel((12, 209), (42, 16, 125, 231))
image.putpixel((264, 143), (122, 136, 25, 213))

image.save('solve.png')

add_metadata("solve.png", "Description", "jctf{not_the_flag}")
add_metadata("solve.png", "Title", "kool_pic")
add_metadata("solve.png", "Author", "anon")
