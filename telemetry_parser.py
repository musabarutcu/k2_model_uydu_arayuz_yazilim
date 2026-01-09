# telemetry_parser.py
# Ham CSV verisini parse eder ve anlamlı bir sözlük (dictionary) döndürür.

import config

class TelemetryParser:
    @staticmethod
    def parse_line(line):
        """
        Gelen virgülle ayrılmış string'i parse eder.
        Dönüş: (success: bool, data: dict)
        """
        try:
            # Satır sonu karakterlerini temizle ve virgülle ayır
            parts = line.strip().split(',')
            
            # Eksik veri kontrolü (En az takım nosuna kadar veri olmalı)
            if len(parts) < len(config.CSV_HEADERS):
                return False, {}

            # Verileri uygun tiplere dönüştür
            data = {
                "paket_no": int(parts[config.IDX_PAKET_NO]),
                "uydu_statu": int(parts[config.IDX_UYDU_STATU]),
                "hata_kodu": parts[config.IDX_HATA_KODU], # String olarak kalabilir (01001 gibi)
                "saat": parts[config.IDX_SAAT],
                "basinc_1": float(parts[config.IDX_BASINC_1]),
                "basinc_2": float(parts[config.IDX_BASINC_2]),
                "yukseklik_1": float(parts[config.IDX_YUKSEKLIK_1]),
                "yukseklik_2": float(parts[config.IDX_YUKSEKLIK_2]),
                "irtifa_farki": float(parts[config.IDX_IRTIFA_FARKI]),
                "inis_hizi": float(parts[config.IDX_INIS_HIZI]),
                "sicaklik": float(parts[config.IDX_SICAKLIK]),
                "pil_gerilimi": float(parts[config.IDX_PIL_GERILIMI]),
                "gps_lat": float(parts[config.IDX_GPS_LAT]),
                "gps_long": float(parts[config.IDX_GPS_LONG]),
                "gps_alt": float(parts[config.IDX_GPS_ALT]),
                "pitch": float(parts[config.IDX_PITCH]),
                "roll": float(parts[config.IDX_ROLL]),
                "yaw": float(parts[config.IDX_YAW]),
                "rhrh": parts[config.IDX_RHRH],
                "iot_s1": float(parts[config.IDX_IOT_S1]),
                "iot_s2": float(parts[config.IDX_IOT_S2]),
                "takim_no": int(parts[config.IDX_TAKIM_NO])
            }
            return True, data

        except ValueError as e:
            print(f"Parse Hatası (Değer): {e} -> Satır: {line}")
            return False, {}
        except Exception as e:
            print(f"Parse Hatası (Genel): {e}")
            return False, {}