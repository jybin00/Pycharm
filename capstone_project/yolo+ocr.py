import cv2
import numpy as np
import json
import requests
import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40
x, y, dw, dh = 0, 0, 0, 0
counter = 0

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
    # data = image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})


# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)

# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights", "yolov4-tiny-custom.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    if frame is None: break
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

            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * 3*h/4)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    if int(VideoSignal.get(1)) % 399 is 0:
        if x is not 0:
            counter += 1
            crop_img = frame[y:y + dh, x:x + dw]
            cv2.imwrite('/Users/yubeenjo/Desktop/Capstone/오토바이번호판/yolo.jpg', crop_img)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if int(VideoSignal.get(1)) % 1000000 is 0:
        appkey = '128c2166d789c9f1a2ae79a9e5dfcc22'
        if x is not 0:
            image_path = '/Users/yubeenjo/Desktop/Capstone/오토바이번호판/yolo.jpg'
            output = kakao_ocr(image_path, appkey).json()
            print("[OCR] output:\n{}\n".format(json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)))
            temp = output['result']

            # try:
            #     word0 = str(temp[0])
            #     word1 = str(temp[1])
            #     word2 = str(temp[2])
            #     word3 = str(temp[3])
            #
            #     city = word0[word0.find('w') + 10:len(word0) - 2]
            #     province = word1[word1.find('w') + 10:len(word1) - 3]
            #     hangul = word2[word2.find('w') + 10:len(word2) - 2]
            #     num = word3[word3.find('w') + 10:len(word3) - 3]
            #
            #     out1 = city + province
            #     out2 = hangul + num
            #
            #     print(out1)
            #     print(out2)
            #
            # except IndexError:
            #     word0 = str(temp[0])
            #     # word1 = str(temp[1])
            #     # word2 = str(temp[2])
            #     # word3 = str(temp[3])
            #
            #     city = word0[word0.find('w') + 10:len(word0) - 2]
            #     # province = word1[word1.find('w') + 10:len(word1) - 3]
            #     # hangul = word2[word2.find('w') + 10:len(word2) - 2]
            #     # num = word3[word3.find('w') + 10:len(word3) - 3]
            #
            #     out1 = city  # + province
            #     # out2 = hangul + num
            #
            #     # print(word0[word0.find('w') + 10:len(word0) - 3])
            #     # print(word1[word1.find('w') + 9:len(word1) - 2])
            #     # print(word2[word2.find('w') + 9:len(word2) - 2])
            #     # print(word3[word3.find('w') + 9:len(word3) - 2])
            #
            #     print(out1)
            #     # print(out2)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = '%2f' %confidences[i]

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label + str(score), (x, y - 20), cv2.FONT_ITALIC, 1,
            (255, 255, 255), 3)
            print(x, y, w, h)

    # cam = cv2.resize(frame, dsize=(800, 500))
    cv2.imshow("test", frame)

    if cv2.waitKey(1) == 27:
        break

VideoSignal.release()
cv2.destroyAllWindows()




