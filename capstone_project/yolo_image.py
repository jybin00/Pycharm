
import cv2
import numpy as np
from skimage import exposure
from PIL import Image, ImageFilter

# 웹캠 신호 받기
frame = cv2.imread("test.jpeg")
frame = cv2.resize(frame, None, fx=1, fy=1)
print(type(frame))
cv2.imshow('test',frame)

# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights", "yolov4-tiny-custom.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]


h, w, c = frame.shape

# YOLO 입력
blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
True, crop=False)
YOLO_net.setInput(blob)
outs = YOLO_net.forward(output_layers)

class_ids = []
confidences = []
boxes = []

for out in outs:

    for detection in out:

        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.8:
            # Object detected
            global crop_img
            center_x = int(detection[0] * w)
            center_y = int(detection[1] * h)
            dw = int(detection[2] * w)
            dh = int(detection[3] * h)
            # Rectangle coordinate
            x = int(center_x - dw / 2)
            y = int(center_y - dh / 2)
            boxes.append([x, y, dw, dh])
            print("x: {0}, y: {1}, dw: {2}, dh:{3}".format(x, y, dw, dh))
            confidences.append(float(confidence))
            print("confidence:" + str(confidence))
            class_ids.append(class_id)
            crop_img = frame[y:y+dh, x:x+dw]

# cv2.imshow("crop", crop_img)
# contrast limit가 2이고 title의 size는 8X8
clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8,8))

gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
img2 = clahe.apply(gray)
denoised = cv2.fastNlMeansDenoising(img2, None, 8, 7, 21)
# contrast = exposure.equalize_adapthist(gray, clip_limit=0.01)

sharpen = cv2.GaussianBlur(gray, (0, 0), 10)
sharpen2 = cv2.addWeighted(gray, 2.0, sharpen, -1.0, 0)
sharpen = cv2.fastNlMeansDenoising(sharpen, None, 10, 7, 21)
binarized = cv2.adaptiveThreshold(sharpen, 256, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 27, 7)


# cv2.imshow('contrast', contrast)
# cv2.imshow('gray', gray)
dst = np.hstack((gray, sharpen, binarized, img2, denoised, sharpen2))
cv2.imshow('img', dst)
# indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# for i in range(len(boxes)):
#     if i in indexes:
#         x, y, w, h = boxes[i]
#         label = str(classes[class_ids[i]])
#         score = '%2f'%confidences[i]
#
#         # 경계상자와 클래스 정보 이미지에 입력
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
#         cv2.putText(frame, label + str(score), (x, y - 20), cv2.FONT_ITALIC, 1,
#         (255, 255, 255), 3)

# cam = cv2.resize(frame, dsize=(800, 500))
# cv2.imshow("test", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()