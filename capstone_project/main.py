import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from video import *
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
class CWidget(QWidget):
 
    def __init__(self):
        super().__init__()    
        size = QSize(800, 400)
        self.initUI(size)
        self.video = video(self, QSize(self.frm.width(), self.frm.height()))
 
    def initUI(self, size):
        
        vbox = QVBoxLayout()        
        # cam on, off button
        self.btn = QPushButton('단속 시작', self)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.onoffCam)
        vbox.addWidget(self.btn)
                 
        # video area
        self.frm = QLabel(self)     
        self.frm.setFrameShape(QFrame.Panel)
         
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)       
        hbox.addWidget(self.frm, 1)        
        self.setLayout(hbox)
        
        self.setFixedSize(size)
        self.move(100,100)
        self.setWindowTitle('신호위반 단속 프로그램')
        self.setWindowIcon(QIcon('am.png'))
        self.show()
 
    def onoffCam(self, e):
        if self.btn.isChecked():
            self.btn.setText('단속 종료')
            self.video.startCam()
        else:
            self.btn.setText('단속 시작')
            self.video.stopCam()
    '''
    def detectOption(self, id):
        if self.grp.button(id).isChecked():
            self.bDetect[id] = True
        else:
            self.bDetect[id] = False
        #print(self.bDetect)
        self.video.setOption(self.bDetect)
    '''
    def recvImage(self, img):
        self.frm.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self, e):
        self.video.stopCam()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())