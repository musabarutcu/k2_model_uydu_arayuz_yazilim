# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Dark Theme Tasarımı (Fusion Stili + CSS)
    app.setStyle("Fusion")
    dark_stylesheet = """
        QMainWindow { background-color: #2b2b2b; }
        QGroupBox { 
            color: white; 
            font-weight: bold; 
            border: 1px solid #555; 
            margin-top: 10px; 
            padding-top: 10px;
        }
        QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
        QLabel { color: #dddddd; font-family: 'Segoe UI', Arial; }
        QPushButton { background-color: #444; color: white; border-radius: 4px; padding: 6px; }
        QPushButton:hover { background-color: #555; }
        QLineEdit { background-color: #333; color: white; border: 1px solid #555; padding: 4px; }
    """
    app.setStyleSheet(dark_stylesheet)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()