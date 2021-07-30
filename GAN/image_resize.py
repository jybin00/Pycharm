import os
import glob
from PIL import Image

files = glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/crop_fix/*.jpg')
counter = 0

for f in files:
    counter += 1
    img = Image.open(f)
    img_resize = img.resize((256, 150))
    title, ext = os.path.splitext(f)
    img_resize.save('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/resize/'+str(counter) + ext)
    print(str(counter/574*100)+"% completed")