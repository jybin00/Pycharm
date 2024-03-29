import cv2  # 사진 조작 및 욜로를 위한 모듈
import numpy as np  # 행렬 연산을 위한 모듈
import json  # 카카오 OCR 프로그램을 위한 json 타입 모듈
import requests  # 카카오 OCR을 위한 모듈
from PIL import ImageFont, ImageDraw, Image
import time  # fps 측정 및 욜로와 OCR 타이밍 제어를 위한 모듈
import re  # 정규식 사용을 위한 모듈

LIMIT_PX = 1024  # 카카오 OCR 최대 픽셀
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40  # 최대 박스 갯수
x, y, dw, dh = 0, 0, 0, 0  # 전역 변수 설정

out1 = ''  # OCR 결과를 담을 스트링 변수
out2 = ''
fps = 0  # 프레임 수를 담을 인트 변수
current_time = 0  # 프레임을 젤 때 쓸 플롯 변수
previous_time = 0
output_words = ['']*40
font2 = ImageFont.truetype('/Library/Fonts/a고딕16.otf', 30)

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
VideoSignal = cv2.VideoCapture(0) # "http://192.168.55.160:8081")

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
    current_time = time.time()
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

            if confidence > 0.6:
                print("ih")
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    sec = current_time - previous_time
    previous_time = current_time
    fps = round(1/sec, 1)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]

            if int(time.time()) % 3 is 0:
                if x is not 0:
                    crop_img = frame[y:y + dh, x:x + dw]
                    x2, y2, _ = crop_img.shape
                    if x2 > 1 and y2 > 1:
                        crop_img = cv2.resize(crop_img, (0, 0), fx=3, fy=3)
                        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite('/Users/yubeenjo/Desktop/' + str(i) + '.jpg', crop_img)
            if int(time.time()) % 3 is 0:
                appkey = '128c2166d789c9f1a2ae79a9e5dfcc22'
                if x is not 0:
                    image_path = '/Users/yubeenjo/Desktop/' + str(i) + '.jpg'
                    output = kakao_ocr(image_path, appkey).json()
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

                        out1 = city + ' ' + province
                        out2 = hangul + ' ' + num
                        output_words[i] = (out1 + out2)

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
                            output_words[i] = (out1 + out2)
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
                                output_words[i] = out1
                            except IndexError:
                                try:
                                    print("index error3!")
                                    word0 = str(temp[0])

                                    city = word0[word0.find('w') + 10:len(word0) - 3]
                                    city = city.replace(" ", "")

                                    out1 = city
                                    output_words[i] = out1
                                except IndexError:
                                    pass
            label = str(classes[class_ids[i]])
            score = round(confidences[i], 2)

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 20, 255), 4)
            frame = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame)
            out1 = re.sub('[a-zA-z]', '', out1)
            out2 = re.sub('[a-zA-z]', '', out2)
            out1 = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"\ø]', '', out1)
            out2 = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"\ø]', '', out2)
            try:
                output_words[i] = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"\ø]', '', output_words[i])
                output_words[i] = re.sub('[a-zA-z]', '', output_words[i])
                draw.text((x + 160, y - 30), str(i) + ' ' + output_words[i], font=font2, fill=(200, 255, 155))
            except IndexError:
                pass
            # draw.text((x + 160, y - 30), out1 + ' ' + out2, font=font2, fill=(255, 255, 155))
            # print(out1 + ' ' + out2)
            frame = np.array(frame)
            cv2.putText(frame, label + str(score), (x, y - 10), cv2.FONT_ITALIC, 1,
            (255, 255, 255), 2)
            print(x, y, w, h)


    cv2.putText(frame, 'fps: ' + str(fps), (10, 30), cv2.FONT_ITALIC, 1,
                (0, 0, 0), 2)

    # cam = cv2.resize(frame, dsize=(800, 500))
    cv2.imshow("test", frame)

    if cv2.waitKey(1) == 27:
        break

VideoSignal.release()
cv2.destroyAllWindows()




