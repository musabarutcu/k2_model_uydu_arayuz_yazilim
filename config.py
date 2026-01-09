# config.py
# Bu dosya tüm sistem sabitlerini, telemetri indekslerini ve ARAS limitlerini tutar.

# Seri Port Ayarları
BAUD_RATE = 9600 # veya 115200, Xbee/LoRa modülüne göre ayarlanmalı
DEFAULT_PORT = "COM3" # Windows için örnek, Linux için /dev/ttyUSB0

# Takım Bilgisi
TEAM_ID = 12345 # Takım numaranızı buraya girin

# Telemetri CSV İndeksleri (Şartname Madde 2.4'e göre )
# Format: <PAKET NO>, <UYDU STATÜSÜ>, <HATA KODU>, <GÖNDERME SAATİ>, ...
IDX_PAKET_NO = 0
IDX_UYDU_STATU = 1
IDX_HATA_KODU = 2
IDX_SAAT = 3
IDX_BASINC_1 = 4
IDX_BASINC_2 = 5
IDX_YUKSEKLIK_1 = 6
IDX_YUKSEKLIK_2 = 7
IDX_IRTIFA_FARKI = 8
IDX_INIS_HIZI = 9
IDX_SICAKLIK = 10
IDX_PIL_GERILIMI = 11
IDX_GPS_LAT = 12
IDX_GPS_LONG = 13
IDX_GPS_ALT = 14
IDX_PITCH = 15
IDX_ROLL = 16
IDX_YAW = 17
IDX_RHRH = 18
IDX_IOT_S1 = 19
IDX_IOT_S2 = 20
IDX_TAKIM_NO = 21

# CSV Başlıkları (Kayıt için)
CSV_HEADERS = [
    "PAKET_NO", "UYDU_STATU", "HATA_KODU", "SAAT", 
    "BASINC_1", "BASINC_2", "YUKSEKLIK_1", "YUKSEKLIK_2", 
    "IRTIFA_FARKI", "INIS_HIZI", "SICAKLIK", "PIL_GERILIMI", 
    "GPS_LAT", "GPS_LONG", "GPS_ALT", 
    "PITCH", "ROLL", "YAW", "RHRH", 
    "IOT_S1", "IOT_S2", "TAKIM_NO"
]

# ARAS Limitleri (Şartname Madde 2.2 [cite: 411-416])
ARAS_LIMITS = {
    "CARRIER_SPEED_MIN": 12.0,
    "CARRIER_SPEED_MAX": 14.0,
    "PAYLOAD_SPEED_MIN": 6.0,
    "PAYLOAD_SPEED_MAX": 8.0,
}

# Uydu Statü Tanımları (Şartname Madde 2.4 - Uydu Statüsü [cite: 494-499])
STATUS_READY = 0
STATUS_ASCENT = 1
STATUS_MODEL_DESCENT = 2  # Taşıyıcı + Görev Yükü
STATUS_SEPARATION = 3
STATUS_PAYLOAD_DESCENT = 4 # Sadece Görev Yükü
STATUS_RESCUE = 5