
import cv2
import numpy as np


# 웹캠 신호 받기
video = '/Users/yubeenjo/Pycharm/capstone_project/IMG_6957 복사본.MOV'
VideoSignal = cv2.VideoCapture(video)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-tiny-custom_best.weights", "yolov4-tiny-custom.cfg")

# 재생할 파일의 넓이 얻기
width = VideoSignal.get(cv2.CAP_PROP_FRAME_WIDTH)

# 재생할 파일의 높이 얻기
height = VideoSignal.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 재생할 파일의 프레임 레이트 얻기
fps = VideoSignal.get(cv2.CAP_PROP_FPS)

writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"DIVX"), fps, (int(width), int(height)))

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
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)


    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = '%2f' %confidences[i]

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label + str(score), (x, y - 20), cv2.FONT_ITALIC, 1,
            (255, 255, 255), 3)

    writer.write(frame)

    # cam = cv2.resize(frame, dsize=(800, 500))
    cv2.imshow("test", frame)

    if cv2.waitKey(1) == 27:
        break

VideoSignal.release()
writer.release()
cv2.destroyAllWindows()