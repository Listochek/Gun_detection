import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from ultralytics import YOLO
from path_data import path_to_model, path_to_video, path_to_save, saver_videos
from notification import send_email
import cv2
import cvzone
import math

CLASS_NAMES = ['gun']
WIDTH_VIDEO = 1280
HEIGHT_VIDEO = 720
IOU_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.5

class VideoWidget(QWidget):
    def __init__(self):
        print("Starting video")
        super().__init__()

        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

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

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2, = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                cvzone.cornerRect(img, (x1, y1, w, h), colorR=(255, 100, 255), colorC=(200, 150, 255))
                conf = math.ceil(box.conf[0] * 100) / 100

                cls = int(box.cls[0])
                cvzone.putTextRect(img, f'{CLASS_NAMES[cls]} {conf}', (max(0, x1), max(0, y1)))
                if CLASS_NAMES[cls] == 'gun':
                    gun_counter += 1   
                    if gun_counter == 20:
                        #send_email()
                        gun_counter = 0

            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            pixmap = QPixmap.fromImage(q_img)
            self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("logging video")
    window = VideoWidget()
    window.show()
    sys.exit(app.exec_())
