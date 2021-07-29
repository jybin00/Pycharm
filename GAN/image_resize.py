import os
import glob
from PIL import Image

files = glob.glob('./data/temp/images/*.jpg')

for f in files:
    img = Image.open(f)
    img_resize = img.resize((int(img.width / 2), int(img.height / 2)))
    title, ext = os.path.splitext(f)
    img_resize.save(title + '_half' + ext)