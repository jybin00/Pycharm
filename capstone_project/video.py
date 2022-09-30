import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import time
import numpy as np

# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-custom_best.weights", "yolov4-obj.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]


class video(QObject):

    sendImage = pyqtSignal(QImage)
 
    def __init__(self, widget, size):
        super().__init__()
        self.widget = widget
        self.size = size
        self.sendImage.connect(self.widget.recvImage)

    def setOption(self, option):
        self.option = option        
 
    def startCam(self):
        try:
            pass
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()
            print("단속 시작")
 
    def stopCam(self):        
        self.bThread = False
        bopen = False
        print(bopen)
        try:
            bopen = self.cap.isOpened()
        except Exception as e:
            print('Error cam not opened')
        else:
            self.cap.release()
 
    def threadFunc(self):
        while self.bThread:
            self.cap = cv2.VideoCapture(0)
            ok, frame = self.cap.read()
            h, w, c = frame.shape

            # YOLO 입력
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
                        dw = int(detection[2] * 2 * w / 3)
                        dh = int(detection[3] * 2 * h / 3)
                        # Rectangle coordinate
                        x = int(center_x - dw / 2)
                        y = int(center_y - dh / 2)
                        boxes.append([x, y, dw, dh])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.8)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    score = '%2f' % confidences[i]
                    print(x, y, label, score)

                    # 경계상자와 클래스 정보 이미지에 입력
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                    cv2.putText(frame, label + str(score), (x, y - 20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)
                    print("번호판 감지")

            bytesPerLine = w * c
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #cv2.imshow("단속화면", frame)
            Img = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
            resizeImg = Img.scaled(self.size.width(), self.size.height(), Qt.KeepAspectRatio)
            self.sendImage.emit(resizeImg)
            time.sleep(0.01)
            if self.bThread == False:
                break

        print('단속 종료')
