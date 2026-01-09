# ui_components/video_widget.py
import cv2
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt
import datetime

class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.video_label = QLabel("Kamera Bekleniyor...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #555;")
        self.video_label.setMinimumSize(320, 240)
        
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

        # Kamera ve Kayıt Ayarları
        self.cap = cv2.VideoCapture(0) # 0: Varsayılan Webcam
        
        # Video Kaydedici (VideoWriter)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        self.out = cv2.VideoWriter(f'flight_video_{timestamp}.avi', fourcc, 20.0, (640, 480))

        # Timer ile kareleri güncelle
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30) # ~30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Kayıt et
            self.out.write(frame)

            # PyQt formatına çevir (BGR -> RGB)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Ekrana bas (Scaled content)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.video_label.width(), self.video_label.height(), 
                Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.cap.release()
        self.out.release()