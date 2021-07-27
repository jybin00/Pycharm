import os
from PIL import Image, ImageFilter
import cv2
import numpy as np
import glob

global counter
counter = 0
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights", "yolov4-tiny-custom.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

for infile in glob.glob('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/백백업/*.jpg'):
    counter += 1
    file, ext = os.path.splitext(infile)
    frame = cv2.imread(infile)
    frame = cv2.resize(frame, None, fx=2, fy=2)
    print(file)

    # 웹캠 프레임
    if frame is None: break
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                global crop_img
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                if y + dh > h or x + dw > w or x < 0 or y < 0:
                    crop_img = frame
                else:
                    crop_img = frame[y:y + dh, x:x + dw]
                print(x, y, dw, dh)
                print(len(crop_img))

    if len(crop_img) > 11:
        cv2.imwrite(file + '_crop.jpg', crop_img)
    else:
        pass

cv2.waitKey(0)
cv2.destroyAllWindows()

