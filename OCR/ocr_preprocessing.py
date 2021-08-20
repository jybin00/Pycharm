import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image, ImageFilter

counter = 0
crop_image = np.empty(100, dtype=object)
font = cv2.FONT_HERSHEY_PLAIN

def binary_image():
    global counter
    for infile in glob.glob('/Users/yubeenjo/Desktop/28.jpg'):
        file, ext = os.path.splitext(infile)
        img = cv2.imread(infile, cv2.IMREAD_GRAYSCALE)
        img = cv2.GaussianBlur(img, (5, 5), 0, 0)
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        img2 = img.copy()
        # img = cv2.equalizeHist(img)
        img2 = cv2.resize(img2, dsize=(0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        img = cv2.resize(img, dsize=(0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
        h0, w0 = img.shape
        kernel = np.ones((4, 4), np.uint8)
        img2 = cv2.morphologyEx(img2, cv2.MORPH_GRADIENT, kernel)
        cv2.imshow("gradient", img2)

        thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                             cv2.THRESH_BINARY, 51, 15)
        cv2.imshow('thresh1', thresh1)
        thresh3 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 51, 0)
        cv2.imshow('thresh3', thresh3)
        kernel = np.ones((5, 11), np.uint8)
        closing = cv2.morphologyEx(thresh3, cv2.MORPH_CLOSE, kernel)
        cv2.imshow('closing', closing)
        # ret, th6 = cv2.threshold(blur, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        thresh2 = thresh1.copy()
        thresh2 = ~thresh2
        thresh1 = ~thresh1
        thresh1 = cv2.dilate(thresh1, kernel, iterations=1)
        kernel = np.ones((10, 20), np.uint8)

        closing2 = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        thresh1 = cv2.dilate(thresh1, kernel, iterations=2)
        # thresh2 = cv2.dilate(thresh2, kernel, iterations=1)
        cv2.imshow('thresh original2', closing2)

        thresh2 = ~thresh2
        # Find the contours on the inverted binary image, and store them in a list
        # Contours are drawn around white blobs.
        # hierarchy variable contains info on the relationship between the contours
        contours, hierarchy = cv2.findContours(closing2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)

        # Draw the contours (in red) on the original image and display the result
        # Input color code is in BGR (blue, green, red) format
        # -1 means to draw all contours
        with_contours = cv2.drawContours(img2, contours, -1, (10, 10, 10), 4)
        cv2.drawContours(thresh2, contours, -1, (10, 0, 0), 1)
        # Draw a bounding box around all contours
        for c in contours:
            global crop_image

            x, y, w, h = cv2.boundingRect(c)

            # Make sure contour area is large enough
            if (cv2.contourArea(c)) > 1:
                if w/w0 > 0.07 and h/h0 < 0.45 and w/w0 < 0.25 and h/h0 > 0.07:
                    crop_image[counter] = img[y: y + h, x: x + w]
                    cv2.imshow(str(counter), crop_image[counter])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (10, 200, 10), 1)
                    cv2.putText(img, str(counter), (x, y), font, 1, (10, 200, 10), 2)
                    print(counter, x, y, w/w0, h/h0)
                    print(cv2.contourArea(c))

                    counter += 1
        cv2.imshow('thresh', thresh2)
        cv2.imshow('bounding box', img)
        # cv2.imshow('histogram ', img2)
        # cv2.imshow('contour', with_contours)
        cv2.imwrite('thresh.jpg', thresh2)
        cv2.waitKey()
        # cv2.imwrite('thresh.png', thresh1)
        # for i in range(len(crop_image)):
        #     plt.subplot(10, 10, i+1)
        #     plt.imshow(crop_image[i], 'gray')
        #
        # plt.show()


        #
        # blur = Image.fromarray(np.uint8(blur))
        # filter_img2 = blur.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # filter_img2.save('edge_enhance.png')
        # r = filter_img2.convert('L').point(fn, mode='1')
        # r.save('binary.png')
        # r.save('foo.png')


binary_image()