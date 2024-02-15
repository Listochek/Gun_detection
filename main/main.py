<<<<<<< Updated upstream
=======
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSlider
>>>>>>> Stashed changes
from ultralytics import YOLO
from path_data import path_to_model
from path_data import path_to_video
from path_data import path_to_save
from path_data import saver_videos

from notification import send_email

import time
import cv2
import cvzone
import math

# путь до модели
model = YOLO(path_to_model)
#путь до видео
cap = cv2.VideoCapture(path_to_video)

<<<<<<< Updated upstream
classNames = ['gun']
# настройки видео
width_video = 1280
height_video = 720

cap.set(3, width_video)
cap.set(4, height_video)
=======
class VideoWidget(QWidget):
    def __init__(self):
        print("Gun_tetection>> Запуск класса...")
        super().__init__()

        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.detected_objects_label = QLabel(self)
        layout.addWidget(self.detected_objects_label)

        font = self.detected_objects_label.font()
        font.setPointSize(16)
        self.detected_objects_label.setFont(font)

        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(int(CONFIDENCE_THRESHOLD * 100))
        self.confidence_slider.valueChanged.connect(self.update_confidence_threshold)
        layout.addWidget(self.confidence_slider)

        self.threshold_label = QLabel(self)
        self.update_threshold_label()
        layout.addWidget(self.threshold_label)

        self.cap = cv2.VideoCapture(path_to_video)
        self.cap.set(3, WIDTH_VIDEO)
        self.cap.set(4, HEIGHT_VIDEO)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.model = YOLO(path_to_model)

    def update_frame(self):
        success, img = self.cap.read()
        if success:
            self.process_frame(img)
            if saver_videos:
                size_video = (WIDTH_VIDEO, HEIGHT_VIDEO)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(path_to_save, fourcc, 30.0, size_video)
                pass

    def process_frame(self, img):
        gun_counter = 0
        results = self.model(img, stream=True, verbose=False, iou=IOU_THRESHOLD, conf=CONFIDENCE_THRESHOLD)
>>>>>>> Stashed changes

def main():
    if saver_videos == True:
        size_video = (width_video, height_video)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path_to_save, fourcc, 30.0, size_video)
    gun_counter = 0
    while True:
        success, img = cap.read()
        results = model(img, stream=True, verbose=False, iou=0.4, conf=0.5)
    
        for r in results:
            boxes = r.boxes
            
            for box in boxes:
                x1, y1, x2, y2, = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

<<<<<<< Updated upstream
                cvzone.cornerRect(img, (x1, y1, w, h), colorR=(255, 100, 255), colorC=(200, 150, 255))
                conf = math.ceil(box.conf[0] * 100) / 100
                
                cls = int(box.cls[0])
                cvzone.putTextRect(img, f'{classNames[cls]}{conf}', (max(0, x1), max(0, y1)))
                if classNames[cls] == 'gun':
                    gun_counter += 1
               
                
                if gun_counter == 20:
                    #send_email()
                    gun_counter = 0
            if saver_videos == True:
                out.write(img)
=======
                if box.conf[0] >= CONFIDENCE_THRESHOLD:
                    cvzone.cornerRect(img, (x1, y1, w, h), colorR=(0, 0, 255), colorC=(0, 0, 255))
                    conf = math.ceil(box.conf[0] * 100) / 100

                    cls = int(box.cls[0])
                    cvzone.putTextRect(img, f'{CLASS_NAMES[cls]} {conf}', (max(0, x1), max(0, y1)))
                    if CLASS_NAMES[cls] == 'gun':
                        gun_counter += 1

            self.detected_objects_label.setText(f'Обнаружено: {gun_counter}')
>>>>>>> Stashed changes

        try: 
            cv2.imshow('Image', img)
            cv2.waitKey(1)
        except:
            cap.release() 
            cv2.destroyAllWindows()
            return

<<<<<<< Updated upstream
main()
=======
            pixmap = QPixmap.fromImage(q_img)
            self.label.setPixmap(pixmap)

    def update_confidence_threshold(self, value):
        global CONFIDENCE_THRESHOLD
        CONFIDENCE_THRESHOLD = value / 100.0
        self.update_threshold_label()
    
    def update_threshold_label(self):
        font = self.threshold_label.font()
        font.setPointSize(16)
        self.threshold_label.setFont(font)
        self.threshold_label.setText(f'Мин. порог: {self.confidence_slider.value()}%')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("Gun_tetection>> __main__ запущен!")
    window = VideoWidget()
    window.show()
    sys.exit(app.exec_())
    print("Gun_tetection>> __main__ закончен!")
>>>>>>> Stashed changes