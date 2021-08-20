import cv2
import numpy as np

img = cv2.imread('/Users/yubeenjo/Pycharm/capstone_project/2.jpg')
img = cv2.resize(img, dsize=(0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
edges = cv2.Canny(img, 150, 250, apertureSize = 3)
cv2.imshow('canny', edges)
gray = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
minLineLength = 10
maxLineGap = 8

lines = cv2.HoughLinesP(edges, 1, np.pi/360, 110, minLineLength, maxLineGap)
for i in range(len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)


cv2.imshow('img1',img)
cv2.waitKey(0)
cv2.destroyAllWindows()