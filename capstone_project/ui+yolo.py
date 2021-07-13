import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import numpy as np

running = False

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-custom_best.weights","yolov4-obj.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

def run():
    global classes
    global output_layers
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(width, height)
    while running:
        ret, frame = cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = img.shape
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
                        dw = int(detection[2] * 2*w/3)
                        dh = int(detection[3] * 2*h/3)
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
                    labels = str(classes[class_ids[i]])
                    score = '%2f' %confidences[i]

                    # 경계상자와 클래스 정보 이미지에 입력
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                    cv2.putText(frame, labels + str(score), (x, y - 20), cv2.FONT_ITALIC, 0.5,
                    (255, 255, 255), 1)

            qImg = QtGui.QImage(frame.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)

        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()
    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")

def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())

# # 웹캠 신호 받기
# VideoSignal = cv2.VideoCapture(0)
# # YOLO 가중치 파일과 CFG 파일 로드
# YOLO_net = cv2.dnn.readNet("yolov4-custom_best.weights","yolov4-obj.cfg")
#
# # YOLO NETWORK 재구성
# classes = []
# with open("obj.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]
# layer_names = YOLO_net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]
#
# while True:
#     # 웹캠 프레임
#     ret, frame = VideoSignal.read()
#     h, w, c = frame.shape
#
#     # YOLO 입력
#     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
#     True, crop=False)
#     YOLO_net.setInput(blob)
#     outs = YOLO_net.forward(output_layers)
#
#     class_ids = []
#     confidences = []
#     boxes = []
#
#     for out in outs:
#
#         for detection in out:
#
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#
#             if confidence > 0.5:
#                 # Object detected
#                 center_x = int(detection[0] * w)
#                 center_y = int(detection[1] * h)
#                 dw = int(detection[2] * 2*w/3)
#                 dh = int(detection[3] * 2*h/3)
#                 # Rectangle coordinate
#                 x = int(center_x - dw / 2)
#                 y = int(center_y - dh / 2)
#                 boxes.append([x, y, dw, dh])
#                 confidences.append(float(confidence))
#                 class_ids.append(class_id)
#     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.8)
#
#
#     for i in range(len(boxes)):
#         if i in indexes:
#             x, y, w, h = boxes[i]
#             label = str(classes[class_ids[i]])
#             score = '%2f' %confidences[i]
#
#             # 경계상자와 클래스 정보 이미지에 입력
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
#             cv2.putText(frame, label + str(score), (x, y - 20), cv2.FONT_ITALIC, 0.5,
#             (255, 255, 255), 1)
#
#     cam = cv2.resize(frame, dsize=(640, 480))
#     cv2.imshow("test", cam)
#
#     if cv2.waitKey(100) > 0:
#         break