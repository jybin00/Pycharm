import cv2  # 화면에 표시하기 위한 모듈
import numpy as np  # 행렬 계산을 위한 모듈
import pytesseract  # OCR을 하기 위한 모듈
from PIL import Image

# yolo 모델 로드
net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights",'yolov4-tiny-custom.cfg')
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readline()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

crop_img = []
ocr = ''
img = cv2.imread("1.jpg")
img = cv2.resize(img, None, fx=2, fy=2)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# 정보를 화면에 표시
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # 좌표
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            crop_img = img[y:y+h, x:x+w]
            ocr = pytesseract.image_to_string(crop_img, lang='kor')

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y), font, 3, color, 2)
        cv2.putText(img, ocr, (x, y), font, 3, color, 2)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()