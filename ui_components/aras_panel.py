# ui_components/aras_panel.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
import config

class ARASPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.indicators = {}
        
        # ARAS Kuralları Etiketleri
        rules = [
            ("TAŞIYICI HIZI", "carrier_speed"), # 12-14 m/s
            ("GÖREV YÜKÜ HIZI", "payload_speed"), # 6-8 m/s
            ("BASINÇ VERİSİ", "pressure"), # Geliyor mu?
            ("KONUM (GPS)", "gps"), # Geliyor mu?
            ("AYRILMA", "separation"), # Statü değişti mi?
            ("FİLTRE MODÜLÜ", "filter") # Hata kodu var mı?
        ]

        for i, (text, key) in enumerate(rules):
            lbl_title = QLabel(text)
            lbl_status = QLabel("BEKLİYOR")
            lbl_status.setStyleSheet("background-color: gray; color: white; padding: 5px;")
            lbl_status.setFixedSize(100, 30)
            
            layout.addWidget(lbl_title, i, 0)
            layout.addWidget(lbl_status, i, 1)
            self.indicators[key] = lbl_status

        self.setLayout(layout)

    def set_status(self, key, is_ok):
        label = self.indicators.get(key)
        if label:
            if is_ok:
                label.setText("NORMAL")
                label.setStyleSheet("background-color: green; color: white; padding: 5px; font-weight: bold;")
            else:
                label.setText("HATA!")
                label.setStyleSheet("background-color: red; color: white; padding: 5px; font-weight: bold;")

    def update_aras(self, data):
        """
        ARAS Mantığı (Şartname Madde 2.2)
        """
        status = data['uydu_statu']
        speed = data['inis_hizi']
        
        # 1. Taşıyıcı İniş Hızı (Statü 2 ise kontrol et: 12-14 m/s) [cite: 411]
        if status == config.STATUS_MODEL_DESCENT:
            check_c_speed = config.ARAS_LIMITS["CARRIER_SPEED_MIN"] <= speed <= config.ARAS_LIMITS["CARRIER_SPEED_MAX"]
            self.set_status("carrier_speed", check_c_speed)
        else:
            self.set_status("carrier_speed", True) # İlgili fazda değilse yeşil kalabilir veya gri

        # 2. Görev Yükü İniş Hızı (Statü 4 ise kontrol et: 6-8 m/s) [cite: 412]
        if status == config.STATUS_PAYLOAD_DESCENT:
            check_p_speed = config.ARAS_LIMITS["PAYLOAD_SPEED_MIN"] <= speed <= config.ARAS_LIMITS["PAYLOAD_SPEED_MAX"]
            self.set_status("payload_speed", check_p_speed)
        else:
            self.set_status("payload_speed", True)

        # 3. Basınç Verisi (Sıfırdan büyükse geliyor kabul edilir) [cite: 413]
        self.set_status("pressure", data['basinc_1'] > 0)

        # 4. Konum (GPS) (Lat/Long 0 değilse) [cite: 414]
        self.set_status("gps", data['gps_lat'] != 0 and data['gps_long'] != 0)

        # 5. Ayrılma Durumu (Statü 3 veya daha büyükse ayrılmıştır) [cite: 415]
        # Eğer manuel ayrılma komutu yollandıysa ve hala statü < 3 ise kırmızı yanmalı (Bu mantık main'de flag ile yönetilebilir)
        self.set_status("separation", True) # Varsayılan yeşil, komut mantığı main'de eklenebilir.

        # 6. Filtre Modülü (Hata kodunun ilgili bitine bakılabilir) [cite: 416]
        # Örn: Hata kodu "00001" ise son bit hata
        self.set_status("filter", True) # Detaylı bit kontrolü eklenebilir.