# serial_interface.py
# Seri port haberleşmesini yönetir. QThread kullanarak arayüzü dondurmaz.

from PyQt6.QtCore import QThread, pyqtSignal
import serial
import time
import config

class SerialInterface(QThread):
    data_received = pyqtSignal(str) # Ham veriyi main'e gönderir
    connection_status = pyqtSignal(bool, str) # Bağlantı durumu

    def __init__(self):
        super().__init__()
        self.port = config.DEFAULT_PORT
        self.baud = config.BAUD_RATE
        self.serial_conn = None
        self.is_running = False

    def run(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baud, timeout=1)
            self.is_running = True
            self.connection_status.emit(True, f"Bağlandı: {self.port}")
            
            while self.is_running:
                if self.serial_conn.in_waiting:
                    try:
                        line = self.serial_conn.readline().decode('utf-8', errors='ignore')
                        if line:
                            self.data_received.emit(line)
                    except Exception as e:
                        print(f"Okuma Hatası: {e}")
                else:
                    time.sleep(0.01) # CPU'yu yormamak için kısa bekleme

        except serial.SerialException as e:
            self.connection_status.emit(False, str(e))
            self.is_running = False

    def send_command(self, command):
        """Komut gönderme (TX)"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                # Komut sonuna satır sonu ekleyerek gönder
                full_cmd = f"{command}\n"
                self.serial_conn.write(full_cmd.encode('utf-8'))
                print(f"Komut Gönderildi: {full_cmd}")
            except Exception as e:
                print(f"Gönderme Hatası: {e}")

    def stop(self):
        self.is_running = False
        if self.serial_conn:
            self.serial_conn.close()
        self.wait()