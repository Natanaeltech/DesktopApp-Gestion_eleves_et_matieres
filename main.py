import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow
from gui.main_window import MainWindow

class MyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.login_window = None
        self.main_window = None
        self.show_login()

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.finished.connect(self.on_login_finished)
        self.login_window.show()

    def on_login_finished(self, result):
        if result == LoginWindow.DialogCode.Accepted:
            self.main_window = MainWindow()
            self.main_window.destroyed.connect(self.on_main_closed)
            self.main_window.show()
        else:
            self.quit()

    def on_main_closed(self):
        self.show_login()

if __name__ == "__main__":
    app = MyApp(sys.argv)
    sys.exit(app.exec())