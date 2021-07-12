import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import time
 
class video(QObject):
 
    sendImage = pyqtSignal(QImage)
 
    def __init__(self, widget, size):
        super().__init__()
        self.widget = widget
        self.size = size
        self.sendImage.connect(self.widget.recvImage)        
                 
        files = ['haarcascade_fullbody.xml',
                'haarcascade_upperbody.xml',
                'haarcascade_lowerbody.xml',
                'haarcascade_frontalface_default.xml',
                'haarcascade_eye.xml',
                'haarcascade_eye_tree_eyeglasses.xml',
                'haarcascade_smile.xml']
      
        self.filters = []
        for i in range(len(files)):
            filter = cv2.CascadeClassifier(files[i])
            self.filters.append(filter)     
 
        self.option = [False for i in range(len(files))]
        self.color = [QColor(255,0,0), QColor(255,128,0), QColor(255,255,0), QColor(0,255,0), QColor(0,0,255), QColor(0,0,128), QColor(128,0,128)]        
             
    def setOption(self, option):
        self.option = option        
 
    def startCam(self):
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()
 
    def stopCam(self):        
        self.bThread = False
        bopen = False
        try:
            bopen = self.cap.isOpened()
        except Exception as e:
            print('Error cam not opened')
        else:
            self.cap.release()
 
    def threadFunc(self):
        while self.bThread:
            ok, frame = self.cap.read()
            if ok:
                # detect image                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                for i in range(len(self.filters)):
                    if self.option[i]:
                        detects = self.filters[i].detectMultiScale(gray, 1.1, 5)
                        for (x, y, w, h) in detects:
                            r = self.color[i].red()
                            g = self.color[i].green()
                            b = self.color[i].blue()
                            cv2.rectangle(frame, (x,y),(x+w,y+h), (b,g,r), 2)              
 
                # create image
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytesPerLine = ch * w
                img = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
                resizedImg = img.scaled(self.size.width(), self.size.height(), Qt.KeepAspectRatio)
                self.sendImage.emit(resizedImg)
            else:
                print('cam read error')
 
            time.sleep(0.01)
 
        print('thread finished')