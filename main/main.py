# Импорт необходимых библиотек
import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QSizePolicy
from ultralytics import YOLO
from path_data import path_to_model, path_to_video, path_to_save, saver_videos, path_to_videos
from notification import send_email
import cv2
import cvzone
import math


# Константы и настройки
CLASS_NAMES = ['gun']
WIDTH_VIDEO = 1280
HEIGHT_VIDEO = 720
IOU_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.5

# Класс виджета для обработки видео
class VideoWidget(QWidget):
    def __init__(self):
        print("Gun_detection>> Запуск класса...")
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                color: #333333;
                font-family: 'Arial';
                font-size: 12px;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #E6E6E6;
                border: 1px solid #BDBDBD;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
            }
            QSlider::handle:horizontal {
                background-color: #BDBDBD;
                border: 1px solid #9E9E9E;
                width: 18px;
                margin: -2px 0; 
                border-radius: 3px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #BDBDBD;
                height: 8px;
                background: #E6E6E6;
                margin: 2px 0;
            }
        """)

        # Создание виджета для отображения видеокадров
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Создание виджета для отображения количества обнаруженных объектов
        self.detected_objects_label = QLabel(self)
        layout.addWidget(self.detected_objects_label)

        # Установка шрифта для метки с количеством объектов
        font = self.detected_objects_label.font()
        font.setPointSize(16) 
        self.detected_objects_label.setFont(font)

        # Создание ползунка для управления минимальным порогом уверенности
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(int(CONFIDENCE_THRESHOLD * 100))
        self.confidence_slider.valueChanged.connect(self.update_confidence_threshold)

        # Установка фиксированной ширины ползунка
        self.confidence_slider.setFixedWidth(150)

        # Добавление ползунка к вертикальному лейауту
        layout.addWidget(self.confidence_slider)

        # Создание метки для отображения текущего порога уверенности
        self.threshold_label = QLabel(self)
        self.update_threshold_label()
        layout.addWidget(self.threshold_label)

        # Горизонтальный лейаут для кнопок видео
        button_layout = QHBoxLayout()

        # Динамическое добавление кнопок для каждого видео в папке
        video_files = [f for f in os.listdir(path_to_videos) if f.endswith(".mp4")]
        self.video_buttons = []
        for video_file in video_files:
            video_button_name = os.path.splitext(video_file)[0]  # Убираем расширение файла
            video_button = QPushButton(video_button_name)   
            video_button.clicked.connect(lambda _, video=video_file: self.play_video(video))
            button_layout.addWidget(video_button)
            self.video_buttons.append(video_button)

        # Добавление горизонтального лейаута в основной вертикальный лейаут
        layout.addLayout(button_layout)

        # Инициализация переменных для работы с видео
        self.cap = cv2.VideoCapture(path_to_video)
        self.cap.set(3, WIDTH_VIDEO)
        self.cap.set(4, HEIGHT_VIDEO)

        # Инициализация таймера для обновления кадров
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Инициализация модели YOLO
        self.model = YOLO(path_to_model)

        # Установка заголовка окна
        self.setWindowTitle("Gun_Detector")

    # Метод для обновления кадра
    def update_frame(self):
        success, img = self.cap.read()
        if success:
            self.process_frame(img)
            if saver_videos:
                size_video = (WIDTH_VIDEO, HEIGHT_VIDEO)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(path_to_save, fourcc, 30.0, size_video)

    # Метод для обработки кадра
    def process_frame(self, img):
        gun_counter = 0
        
        clarity = 0.2 #коффицент прозрачности выделяемого ббоксика
        results = self.model(img, verbose=False, iou=IOU_THRESHOLD, conf=CONFIDENCE_THRESHOLD)


        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2, = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                if box.conf[0] >= CONFIDENCE_THRESHOLD:
                    cls = int(box.cls[0])
                    overlay = img.copy()
                    cvzone.cornerRect(img, (x1, y1, w, h), colorR=(0, 0, 255), colorC=(0, 0, 255)) # выделение рамки ббокса
                    cv2.rectangle(overlay, (x1, y1, w, h), thickness=cv2.FILLED, color=(10, 10, 150)) # закрашивание ббоксика
                    cv2.addWeighted(overlay, clarity, img, 1 - clarity, 0, img) # наложение закрашенной области

                    conf = math.ceil(box.conf[0] * 100) #точность predicta модели

                    cvzone.putTextRect(img, f'{CLASS_NAMES[cls]} {conf}%', # текст надпеси у ббокса
                                       (max(0, x1), max(0, y1)), # расположение надписи
                                       colorR=(0, 0, 255), #цвет фона надписи
                                       scale=2, thickness=2 )# ширина и высота надписи
                    
                    if CLASS_NAMES[cls] == 'gun': # счетчик кадров с оружием 
                        gun_counter += 1
                        if gun_counter == 20:
                            #send_email #отправка уведомления на почту
                            gun_counter = 0

            self.detected_objects_label.setText(f'Обнаружено: {gun_counter}')

            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            pixmap = QPixmap.fromImage(q_img)
            self.label.setPixmap(pixmap)

    # Метод для обновления порога уверенности
    def update_confidence_threshold(self, value):
        global CONFIDENCE_THRESHOLD
        CONFIDENCE_THRESHOLD = value / 100.0
        self.update_threshold_label()


    # Метод для обновления метки порога
    def update_threshold_label(self):
        font = self.threshold_label.font()
        font.setPointSize(16)
        self.threshold_label.setFont(font)
        self.threshold_label.setText(f'Мин. порог: {self.confidence_slider.value()}%')


    # Метод для воспроизведения выбранного видео
    def play_video(self, video_file):
        video_path = os.path.join(path_to_videos, video_file)
        self.cap.release()
        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(3, WIDTH_VIDEO)
        self.cap.set(4, HEIGHT_VIDEO)
        self.detected_objects_label.setText("Обнаружено: 0")

# Основной блок кода для запуска приложения
if __name__ == '__main__':
    print("Gun_detection>> __main__ запущен!")
    app = QApplication(sys.argv)
    window = VideoWidget()
    window.show()
    sys.exit(app.exec_())
    print("Gun_detection>> __main__ закончен!")