import sys, cv2, numpy, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 상태표시줄
        datetime = QDateTime.currentDateTime()
        self.statusBar().showMessage(datetime.toString('yyyy년 MM월 dd일 hh:mm:ss'))
        # 툴팁
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('단속을 시작하려면 버튼을 누르세요')
        # 버튼
        self.btn1 = QPushButton('단속 시작', self)
        self.btn1.setToolTip('단속을 시작하려면 버튼을 누르세요')
        self.btn1.move(20,20)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(self.start)

        self.btn2 = QPushButton('단속 종료', self)
        self.btn2.move(100,20)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.clicked.connect(self.stop)
        # 감도 조절 slider
        self.sldr = QSlider(Qt.Horizontal, self)
        self.sldr.resize(200,25)
        self.sldr.move(20,50)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(30)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        #단속영상
        self.cpt = cv2.VideoCapture(0)
        self.fps = 24
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_o.jpg',self.img_o)
      
        self.cnt = 0
        self.frame = QLabel(self)
        self.frame.resize(600,400)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)

        self.setWindowTitle('test')
        self.setWindowIcon(QIcon('am.png'))
        self.setGeometry(300, 300, 300, 200)
        self.move(300, 300)
        self.resize(800, 600)
        self.show()

    def setFps(self):
        self.fps = self.sldr.value()
        self.prt.setText("현재 FPS" + str(self.fps))
        self.timer.stop()
        self.timer.start(1000. / self.fps)

    def start(self):
        self.timer = Qtimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
        cam = cv2.flip(cam, 0)
        self.img_p = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('img_p.jpg',self.img_p)
        self.compare(self.img_o, self.img_p)
        self.img_o = self.img_p.copy()
        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Foramt_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

    def stop(self):
        self.frame.setPixmap(Qpixmap.fromImage(QIamge()))
        self.timer.stop()
    
    def compare(self, img_o, img_p):
        err = numpy.sum((img_o.astype("float")-img_p.astype("float")) ** 2)
        err /= float(img_o.shape[0] * img_p.shape[1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


#웹캠 연결 코드 참조
# https://www.youtube.com/watch?v=uiu1asWUx6g&list=PL1eLKSeW1Baj72go6l3gg4C8TXRNUBdMo&index=16

