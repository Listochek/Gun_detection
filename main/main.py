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

classNames = ['gun']
# настройки видео
width_video = 1280
height_video = 720

cap.set(3, width_video)
cap.set(4, height_video)



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

        try: 
            cv2.imshow('Image', img)
            cv2.waitKey(1)
        except:
            cap.release() 
            cv2.destroyAllWindows()
            return

main()