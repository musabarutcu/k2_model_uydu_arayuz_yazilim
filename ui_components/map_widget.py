# ui_components/map_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Koordinat Bilgi Paneli
        self.coord_label = QLabel("GPS: Veri Bekleniyor...")
        self.coord_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #00ff00;")
        self.layout.addWidget(self.coord_label)

        # Basit Scatter Plot (Göreceli Konum)
        self.plot_widget = pg.PlotWidget(title="GPS Konumu (Scatter)")
        self.plot_widget.setBackground('#1e1e1e')
        self.plot_widget.showGrid(x=True, y=True)
        self.scatter = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255))
        self.plot_widget.addItem(self.scatter)
        
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)

    def update_map(self, lat, long, alt):
        self.coord_label.setText(f"LAT: {lat:.6f} | LON: {long:.6f} | ALT: {alt:.2f}")
        
        # Haritaya nokta koy (Basit gösterim için Lat/Long doğrudan X/Y yapıldı)
        # Gerçek uygulamada merkez noktaya göre fark alınarak metre cinsinden çizdirilir.
        self.scatter.addPoints([{'pos': (long, lat), 'data': 1}])