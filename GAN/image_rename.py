import os
import glob
from PIL import Image

files = glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/모자이크/*.jpg')
counter = 0
print(len(files))

for f in files:
    counter += 1
    img = Image.open(f)
    title, ext = os.path.splitext(f)
    img.save('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/fake2/' + str(counter) + ext)
    print(str(counter/294*100)+"% completed")
    img.close()
