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
    for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/조작/clean 복사본/*.jpg'):
        file, ext = os.path.splitext(infile)
        f = open(file + '.txt', 'w')
        f.write("아이글 화이팅~ \n\n")
        img = cv2.imread(infile, cv2.IMREAD_GRAYSCALE)

        img = cv2.equalizeHist(img)
        counter = 0
        # img2 = img.copy()
        # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        # img = cv2.resize(img, dsize=(0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

        kernel = np.ones((4, 4), np.uint8)
        blur = cv2.GaussianBlur(img, (5, 5), 0, 0)
        thresh1 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                             cv2.THRESH_BINARY, 15, 20)
        # ret, thresh2 = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY_INV)
        # ret, thresh3 = cv2.threshold(blur, 150, 255, cv2.THRESH_TRUNC)
        # ret, thresh4 = cv2.threshold(blur, 150, 255, cv2.THRESH_TOZERO)
        # ret, thresh5 = cv2.threshold(blur, 150, 255, cv2.THRESH_TOZERO_INV)
        ret, th6 = cv2.threshold(blur, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # thresh6 = ~thresh2
        thresh1 = ~thresh1
        th6 = cv2.dilate(th6, kernel, iterations=1)
        thresh1 = cv2.dilate(thresh1, kernel, iterations=1)
        # Find the contours on the inverted binary image, and store them in a list
        # Contours are drawn around white blobs.
        # hierarchy variable contains info on the relationship between the contours
        contours, hierarchy = cv2.findContours(thresh1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)

        # Draw the contours (in red) on the original image and display the result
        # Input color code is in BGR (blue, green, red) format
        # -1 means to draw all contours
        # with_contours = cv2.drawContours(thresh1, contours, -1, (255, 0, 255), 1)
        # Draw a bounding box around all contours
        for c in contours:
            global crop_image

            x, y, w, h = cv2.boundingRect(c)

            # Make sure contour area is large enough
            if (cv2.contourArea(c)) > 200 and cv2.contourArea(c) < 2500:
                # crop_image[counter] = img[y: y + h, x: x + w]
                # cv2.imshow(str(counter), crop_image[counter])
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 200, 10), 0 )
                cv2.putText(img, str(counter), (x, y), font, 1, (10, 200, 10), 2)
                f.write("c:%3d  x: %3d y: %3d w: %3d h: %3d \n" % (counter, x, y, w, h))
                print(counter, x, y, w, h)
                print(cv2.contourArea(c))
                counter += 1
        cv2.imwrite(file + 'thresh' + ext, thresh1)
        cv2.imwrite(file+'bounding_box' +ext, img)
        f.write("\n이상한 박스도 포함되어 있습니다! 주의해주세용~")
        f.close()
        # image = [thresh1, thresh2, thresh3, thresh4, thresh5, thresh6, img, img2, th6]

        # cv2.imwrite('thresh.png', thresh1)
        # for i in range(9):
        #     plt.subplot(3,3,i+1)
        #     plt.imshow(image[i], 'gray')
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