import cv2  # 화면에 표시하기 위한 모듈
import numpy as np  # 행렬 계산을 위한 모듈
import pytesseract  # OCR을 하기 위한 모듈
from PIL import ImageFont, ImageDraw, Image
import json
import requests
import sys

def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})


LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

image_path = '/Users/yubeenjo/Pycharm/capstone_project/2.jpg'
# kakao Developers에서 API 키
appkey = '128c2166d789c9f1a2ae79a9e5dfcc22'


# yolo 모델 로드
net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights", 'yolov4-tiny-custom.cfg')
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readline()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

custom_oem_psm_config = r'--oem 3 --psm 11'
crop_img = []
ocr = ''
out1 = ''
out2 = ''
h1 = []
img = cv2.imread("/Users/yubeenjo/Desktop/Capstone/오토바이번호판/백업/29.jpg")
img = cv2.resize(img, None, fx=3, fy=3)
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

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
font2 = ImageFont.truetype('/Library/Fonts/a고딕16.otf', 30)
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        crop_img = img[y: y + h, x: x + w]
        crop_img = cv2.resize(crop_img, (900, 900), None, None)
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        img1 = crop_img
        # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
        # crop_img = clahe.apply(crop_img)
        img2 = crop_img
        crop_img = cv2.GaussianBlur(crop_img, (7, 7), 0, 0)
        img3 = crop_img
        crop_img = cv2.adaptiveThreshold(crop_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY_INV, 39, 12)
        img4 = crop_img
        kernel = np.ones((8, 8), np.uint8)
        crop_img = cv2.dilate(crop_img, kernel, iterations=1)
        img5 = ~crop_img
        h1 = np.hstack([img1, img2, img3, img4, img5])
        ocr = pytesseract.image_to_string(crop_img, lang='kor')
        print(ocr)
        cv2.imwrite('2.jpg', img1)
        output = kakao_ocr(image_path, appkey).json()
        print(output)
        temp = output['result']

        try:
            word0 = str(temp[0])
            word1 = str(temp[1])
            word2 = str(temp[2])
            word3 = str(temp[3])

            city = word0[word0.find('w') + 10:len(word0) - 3]
            city = city.replace(" ", "")
            province = word1[word1.find('w') + 10:len(word1) - 3]
            province = province.replace(" ", "")
            hangul = word2[word2.find('w') + 10:len(word2) - 3]
            hangul = hangul.replace(" ", "")
            num = word3[word3.find('w') + 10:len(word3) - 3]
            num = num.replace(" ", "")

            out1 = city + +' ' + province
            out2 = hangul + ' ' + num

        except IndexError:
            try:
                print("index error!")
                word0 = str(temp[0])
                print(type(word0))
                word1 = str(temp[1])
                word2 = str(temp[2])

                city = word0[word0.find('w') + 10:len(word0) - 3]
                city = city.replace(" ", "")
                province = word1[word1.find('w') + 10:len(word1) - 3]
                province = province.replace(" ", "")
                hangul = word2[word2.find('w') + 10:len(word2) - 3]
                hangul = hangul.replace(" ", "")

                out1 = city + ' ' + province
                out2 = hangul
                pass

            except IndexError:
                try:
                    print("index error2!")
                    word0 = str(temp[0])
                    word1 = str(temp[1])

                    city = word0[word0.find('w') + 10:len(word0) - 3]
                    city = city.replace(" ", "")
                    province = word1[word1.find('w') + 10:len(word1) - 3]
                    province = province.replace(" ", "")

                    out1 = city + ' ' + province
                except IndexError:
                    try:
                        print("index error3!")
                        word0 = str(temp[0])

                        city = word0[word0.find('w') + 10:len(word0) - 3]
                        city = city.replace(" ", "")

                        out1 = city
                    except IndexError:
                        pass

        print(x, y, w, h)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        draw.text((x+140, y-30), out1 + ' ' + out2, font=font2, fill=(255, 255, 255))
        img = np.array(img)
        cv2.putText(img, 'plate', (x, y), font, 3, color, 2)
cv2.imshow('crop', h1)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
