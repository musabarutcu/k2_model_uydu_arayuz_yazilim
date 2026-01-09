# ui_components/command_panel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QLabel, QMessageBox

class CommandPanel(QWidget):
    def __init__(self, serial_interface):
        super().__init__()
        self.serial = serial_interface
        layout = QVBoxLayout()
        
        # Başlık
        layout.addWidget(QLabel("KOMUT PANELİ"))

        # RHRH Girişi [cite: 396]
        rhrh_layout = QHBoxLayout()
        self.txt_rhrh = QLineEdit()
        self.txt_rhrh.setPlaceholderText("Kod: 6G8R")
        btn_send_rhrh = QPushButton("FİLTRE KODU GÖNDER")
        btn_send_rhrh.setStyleSheet("background-color: #007acc; color: white;")
        btn_send_rhrh.clicked.connect(self.send_rhrh)
        
        rhrh_layout.addWidget(self.txt_rhrh)
        rhrh_layout.addWidget(btn_send_rhrh)
        layout.addLayout(rhrh_layout)

        # Manuel Ayrılma [cite: 382]
        self.btn_separate = QPushButton("MANUEL AYRILMA")
        self.btn_separate.setStyleSheet("background-color: darkred; color: white; font-weight: bold; height: 40px;")
        self.btn_separate.clicked.connect(self.send_separation)
        layout.addWidget(self.btn_separate)

        self.setLayout(layout)

    def send_rhrh(self):
        code = self.txt_rhrh.text().strip()
        if len(code) == 4:
            self.serial.send_command(f"RHRH:{code}") # Protokole uygun format
        else:
            QMessageBox.warning(self, "Hata", "Kod 4 haneli olmalı (Örn: 6G8R)")

    def send_separation(self):
        confirm = QMessageBox.question(self, "Onay", "Manuel Ayrılma Komutu Gönderilsin mi?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.serial.send_command("AYRILMA") # Protokole uygun komut