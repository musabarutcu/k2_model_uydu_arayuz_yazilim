# ui_components/simulation_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QTransform, QPolygon
from PyQt6.QtCore import Qt, QPoint

class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.info_label = QLabel("P:0 R:0 Y:0")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.info_label)
        self.setLayout(layout)

    def update_orientation(self, p, r, y):
        self.pitch = p
        self.roll = r
        self.yaw = y
        self.info_label.setText(f"P:{p:.1f}° R:{r:.1f}° Y:{y:.1f}°")
        self.update() # paintEvent'i tetikler

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        center = QPoint(w // 2, h // 2)

        # Arka plan
        painter.fillRect(0, 0, w, h, QColor(30, 30, 30))

        # Koordinat Sistemi Dönüşümü (Roll ve Pitch Görselleştirmesi)
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(self.roll) # Roll hareketi
        # Pitch hareketi görsel olarak okun boyunu kısaltabilir veya yukarı kaydırabilir
        
        painter.setTransform(transform)

        # Uyduyu temsil eden basit bir şekil (Ok/Roket)
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setBrush(QColor(0, 150, 255))
        
        # Basit roket şekli
        points = [
            QPoint(0, -50),
            QPoint(-20, 20),
            QPoint(0, 10),
            QPoint(20, 20)
        ]
        poly = QPolygon(points)
        painter.drawPolygon(poly)