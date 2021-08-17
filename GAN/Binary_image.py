import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image, ImageFilter

counter = 0
crop_image = np.empty(100, dtype=object)

def binary_image():
    for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/조작/crop/15_crop.jpg'):
        file, ext = os.path.splitext(infile)
        img = cv2.imread(infile)
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        #img = cv2.resize(img, dsize=(0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

        kernel = np.ones((2, 2), np.uint16)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img, (5, 5), 0, 0)
        ret, thresh1 = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY)
        ret, thresh2 = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY_INV)
        ret, thresh3 = cv2.threshold(blur, 150, 255, cv2.THRESH_TRUNC)
        ret, thresh4 = cv2.threshold(blur, 150, 255, cv2.THRESH_TOZERO)
        ret, thresh5 = cv2.threshold(blur, 150, 255, cv2.THRESH_TOZERO_INV)
        ret, th6 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh6 = ~thresh2
        th6 = ~th6
        th6 = cv2.dilate(th6, kernel, iterations=1)
        thresh2 = cv2.dilate(thresh2, kernel, iterations=1)
        # Find the contours on the inverted binary image, and store them in a list
        # Contours are drawn around white blobs.
        # hierarchy variable contains info on the relationship between the contours
        contours, hierarchy = cv2.findContours(thresh2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours (in red) on the original image and display the result
        # Input color code is in BGR (blue, green, red) format
        # -1 means to draw all contours
        # with_contours = cv2.drawContours(img2, contours, -1, (255, 0, 255), 3)
        # Draw a bounding box around all contours
        for c in contours:
            global counter
            global crop_image

            x, y, w, h = cv2.boundingRect(c)

            # Make sure contour area is large enough
            if (cv2.contourArea(c)) > 250 and (cv2.contourArea(c)) < 2500:
                crop_image[counter] = img[y: y + h, x: x + w]
                cv2.imshow(str(counter), crop_image[counter])
                counter += 1
                cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 1), 2)
                print(x,y,w,h)
                print(cv2.contourArea(c))
        image = [thresh1, thresh2, thresh3, thresh4, thresh5, thresh6, img, img2, th6]

        # cv2.imwrite('thresh.png', thresh1)
        for i in range(9):
            plt.subplot(3,3,i+1)
            plt.imshow(image[i], 'gray')

        plt.show()


        #
        # blur = Image.fromarray(np.uint8(blur))
        # filter_img2 = blur.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # filter_img2.save('edge_enhance.png')
        # r = filter_img2.convert('L').point(fn, mode='1')
        # r.save('binary.png')
        # r.save('foo.png')


binary_image()