# main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QGroupBox, QLabel, QScrollArea
from PyQt6.QtCore import Qt
import config
from telemetry_parser import TelemetryParser
from serial_interface import SerialInterface
from data_logger import DataLogger
from ui_components.video_widget import VideoWidget
from ui_components.graphs_widget import GraphsWidget
from ui_components.map_widget import MapWidget
from ui_components.simulation_widget import SimulationWidget
from ui_components.aras_panel import ARASPanel
from ui_components.command_panel import CommandPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"TÜRKSAT Model Uydu - YER İSTASYONU - Takım: {config.TEAM_ID}")
        self.setGeometry(100, 100, 1280, 800)

        # Arka Plan Servisleri
        self.parser = TelemetryParser()
        self.logger = DataLogger()
        self.serial = SerialInterface()
        
        # Seri port sinyallerini bağla
        self.serial.data_received.connect(self.process_telemetry)
        self.serial.start() # Dinlemeye başla

        # UI Kurulumu
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # --- SOL SÜTUN ---
        # 1. Video (Sol Üst) [cite: 382]
        gb_video = QGroupBox("Canlı Yayın & Kayıt")
        video_layout = QGridLayout()
        self.video_widget = VideoWidget()
        video_layout.addWidget(self.video_widget)
        gb_video.setLayout(video_layout)
        main_layout.addWidget(gb_video, 0, 0, 1, 1) # Satır 0, Sütun 0

        # 2. ARAS Paneli (Video Altı)
        gb_aras = QGroupBox("ARAS (Alarm Sistemi)")
        aras_layout = QGridLayout()
        self.aras_panel = ARASPanel()
        aras_layout.addWidget(self.aras_panel)
        gb_aras.setLayout(aras_layout)
        main_layout.addWidget(gb_aras, 1, 0, 1, 1)

        # --- ORTA SÜTUN (GRAFİKLER) ---
        gb_graphs = QGroupBox("Canlı Telemetri Grafikleri")
        graphs_layout = QGridLayout()
        self.graphs_widget = GraphsWidget()
        graphs_layout.addWidget(self.graphs_widget)
        gb_graphs.setLayout(graphs_layout)
        main_layout.addWidget(gb_graphs, 0, 1, 2, 1) # 2 Satır kapla

        # --- SAĞ SÜTUN ---
        # 1. Harita ve Simülasyon
        gb_viz = QGroupBox("Görselleştirme")
        viz_layout = QGridLayout()
        self.map_widget = MapWidget()
        self.sim_widget = SimulationWidget()
        viz_layout.addWidget(self.map_widget, 0, 0)
        viz_layout.addWidget(self.sim_widget, 1, 0)
        gb_viz.setLayout(viz_layout)
        main_layout.addWidget(gb_viz, 0, 2, 1, 1)

        # 2. Komut Paneli ve Bonus Veri
        gb_cmd = QGroupBox("Kontrol ve IoT")
        cmd_layout = QGridLayout()
        self.cmd_panel = CommandPanel(self.serial)
        self.lbl_iot = QLabel("IoT Verisi: Bekleniyor...")
        self.lbl_iot.setStyleSheet("font-size: 14px; color: cyan;")
        
        cmd_layout.addWidget(self.cmd_panel, 0, 0)
        cmd_layout.addWidget(self.lbl_iot, 1, 0)
        gb_cmd.setLayout(cmd_layout)
        main_layout.addWidget(gb_cmd, 1, 2, 1, 1)

    def process_telemetry(self, raw_data):
        # 1. Parse Et
        success, data = self.parser.parse_line(raw_data)
        
        if success:
            # 2. Logla
            self.logger.log_data(data)
            
            # 3. UI Güncelle
            self.graphs_widget.update_graphs(data)
            self.map_widget.update_map(data['gps_lat'], data['gps_long'], data['gps_alt'])
            self.sim_widget.update_orientation(data['pitch'], data['roll'], data['yaw'])
            self.aras_panel.update_aras(data)
            
            # IoT Bonus [cite: 398]
            self.lbl_iot.setText(f"IoT S1: {data['iot_s1']} °C | IoT S2: {data['iot_s2']} °C")

    def closeEvent(self, event):
        self.serial.stop()
        self.video_widget.close()
        event.accept()