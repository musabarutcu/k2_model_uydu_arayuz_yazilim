# data_logger.py
# Verileri anlık olarak CSV dosyasına kaydeder.

import csv
import datetime
import os
import config

class DataLogger:
    def __init__(self):
        # Dosya ismi: Tarih_Saat_TakimNo.csv
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{timestamp}_Team{config.TEAM_ID}.csv"
        
        # Dosyayı oluştur ve başlıkları yaz
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(config.CSV_HEADERS)
            
        print(f"Log dosyası oluşturuldu: {self.filename}")

    def log_data(self, parsed_data_dict):
        """Parse edilmiş veriyi sırasına göre dizer ve yazar"""
        try:
            row = [parsed_data_dict.get(key.lower(), 0) for key in config.CSV_HEADERS]
            
            with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row)
        except Exception as e:
            print(f"Kayıt Hatası: {e}")