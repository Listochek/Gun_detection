import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSlider, QPushButton, QHBoxLayout
from ultralytics import YOLO
from path_data import path_to_model, path_to_video, path_to_save, saver_videos, path_to_videos
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

        self.confidence_slider.setFixedWidth(150)

        layout.addWidget(self.confidence_slider)

        self.threshold_label = QLabel(self)
        self.update_threshold_label()
        layout.addWidget(self.threshold_label)
        button_layout = QHBoxLayout()

        video_files = [f for f in os.listdir(path_to_videos) if f.endswith(".mp4")]

        self.video_buttons = []
        for video_file in video_files:
            video_button = QPushButton(video_file)
            video_button.clicked.connect(lambda _, video=video_file: self.play_video(video))
            layout.addWidget(video_button)
            self.video_buttons.append(video_button)

        layout.addLayout(button_layout)
        self.cap = cv2.VideoCapture(path_to_video)
        self.cap.set(3, WIDTH_VIDEO)
        self.cap.set(4, HEIGHT_VIDEO)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.model = YOLO(path_to_model)

        self.setWindowTitle("Gun_Detector")

    def update_frame(self):
        success, img = self.cap.read()
        if success:
            self.process_frame(img)
            if saver_videos:
                size_video = (WIDTH_VIDEO, HEIGHT_VIDEO)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(path_to_save, fourcc, 30.0, size_video)


    def process_frame(self, img):
        gun_counter = 0
        results = self.model(img, verbose=False, iou=IOU_THRESHOLD, conf=CONFIDENCE_THRESHOLD)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2, = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                if box.conf[0] >= CONFIDENCE_THRESHOLD:
                    cvzone.cornerRect(img, (x1, y1, w, h), colorR=(0, 40, 255), colorC=(0, 0, 255))
                    conf = math.ceil(box.conf[0] * 100) / 100

                    cls = int(box.cls[0])
                    cvzone.putTextRect(img, f'{CLASS_NAMES[cls]} {conf}', (max(0, x1), max(0, y1)), colorR=(0, 0, 255))
                    if CLASS_NAMES[cls] == 'gun':
                        gun_counter += 1

            self.detected_objects_label.setText(f'Обнаружено: {gun_counter}')

            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

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

    def play_video(self, video_file):
        video_path = os.path.join(path_to_videos, video_file)
        self.cap.release()
        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(3, WIDTH_VIDEO)
        self.cap.set(4, HEIGHT_VIDEO)
        self.detected_objects_label.setText("Обнаружено: 0")

if __name__ == '__main__':
    print("Gun_tetection>> __main__ запущен!")
    app = QApplication(sys.argv)
    window = VideoWidget()
    window.show()
    sys.exit(app.exec_())
    print("Gun_tetection>> __main__ закончен!")
