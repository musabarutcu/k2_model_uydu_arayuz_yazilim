# ui_components/graphs_widget.py
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QGridLayout
import numpy as np
from collections import deque

class GraphsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        # Veri Tamponları (Son 100 veriyi tutar)
        self.buffer_size = 100
        self.ptr = 0
        self.time_data = deque(maxlen=self.buffer_size)
        self.pressure_data = deque(maxlen=self.buffer_size)
        self.altitude_data = deque(maxlen=self.buffer_size)
        self.speed_data = deque(maxlen=self.buffer_size)
        self.temp_data = deque(maxlen=self.buffer_size)
        self.voltage_data = deque(maxlen=self.buffer_size)

        # Grafikleri Oluştur
        self.p_pressure = self.create_plot("Basınç (Pa)", "r")
        self.p_altitude = self.create_plot("Yükseklik (m)", "g")
        self.p_speed = self.create_plot("İniş Hızı (m/s)", "b")
        self.p_temp = self.create_plot("Sıcaklık (C)", "y")
        self.p_voltage = self.create_plot("Pil (V)", "m")

        # Yerleşim (Layout)
        self.layout.addWidget(self.p_pressure, 0, 0)
        self.layout.addWidget(self.p_altitude, 0, 1)
        self.layout.addWidget(self.p_speed, 1, 0)
        self.layout.addWidget(self.p_temp, 1, 1)
        self.layout.addWidget(self.p_voltage, 2, 0, 1, 2) # Pil grafiği alta geniş

    def create_plot(self, title, color_code):
        plot = pg.PlotWidget(title=title)
        plot.showGrid(x=True, y=True)
        plot.setBackground('#1e1e1e')
        # Eğri referansını sakla
        plot.curve = plot.plot(pen=pg.mkPen(color=color_code, width=2))
        return plot

    def update_graphs(self, data):
        # Zaman ekseni için paket nosu veya basit sayaç kullanılabilir
        self.time_data.append(data['paket_no'])
        
        self.pressure_data.append(data['basinc_1'])
        self.altitude_data.append(data['yukseklik_1'])
        self.speed_data.append(data['inis_hizi'])
        self.temp_data.append(data['sicaklik'])
        self.voltage_data.append(data['pil_gerilimi'])

        # Çizdir
        self.p_pressure.curve.setData(self.time_data, self.pressure_data)
        self.p_altitude.curve.setData(self.time_data, self.altitude_data)
        self.p_speed.curve.setData(self.time_data, self.speed_data)
        self.p_temp.curve.setData(self.time_data, self.temp_data)
        self.p_voltage.curve.setData(self.time_data, self.voltage_data)