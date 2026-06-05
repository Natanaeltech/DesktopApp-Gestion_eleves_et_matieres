from PyQt6.QtWidgets import QApplication
import os

def apply_stylesheet(widget):
    """Applique le style QSS à un widget ou à toute l'application."""
    style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            style = f.read()
            widget.setStyleSheet(style)
    else:
        widget.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #f0f0f0; }
            QPushButton { background-color: #4a6ea9; border: none; padding: 5px; border-radius: 3px; }
            QPushButton:hover { background-color: #5d7fb9; }
            QTableWidget { alternate-background-color: #3c3c3c; }
        """)
