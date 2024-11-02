from PyQt6.QtWidgets import QApplication
import settings
import app_styles
from game_windows.GameWindow import GameWindow
from game_windows.MainWindow import MainWindow


class App(QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)
        self.setStyleSheet(app_styles.app_styles)

        self.main_window = MainWindow(settings.test_settings)
        self.game_window = GameWindow()

        self.windows = {'main_window': self.main_window, 'game_window': self.game_window}

        self.main_window.router = self.windows
        self.game_window.set_router(self.windows)

        self.windows['main_window'].show()
