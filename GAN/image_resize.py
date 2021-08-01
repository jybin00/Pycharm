import os
import glob
from PIL import Image

files = glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/모자이크/*.jpg')
counter = 0

for f in files:
    counter += 1
    img = Image.open(f)
    img_resize = img.resize((254, 150))
    title, ext = os.path.splitext(f)
    img_resize.save('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/모자이/' + str(counter) + ext)
    print(str(counter/574*100)+"% completed")