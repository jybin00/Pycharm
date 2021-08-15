import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image
def canny():
    for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/fake/*.jpg'):
        file, ext = os.path.splitext(infile)
        img = cv2.imread(infile)
        blur = cv2.GaussianBlur(img, (3, 3), 0)
        edge5 = cv2.Canny(blur, 130, 200)

        cv2.imwrite(infile, edge5)

canny()