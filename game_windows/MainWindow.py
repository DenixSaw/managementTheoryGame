from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea
from data.text_data import menu_pages_data, styles, game_mode


class MainWindow(QMainWindow):

    def set_settings(self, settings):
        self._settings = settings

    def _on_choice_button_click(self, choice):
        if choice == 0:
            self._settings['0'] = 0.5
            self._settings['1'] = 0.5
        elif choice == 1:
            self._settings['0'] = 0.34
            self._settings['1'] = 0.66
        elif choice == 2:
            self._settings['0'] = 0.66
            self._settings['1'] = 0.34
        else:
            raise ValueError("Неверный выбор")
        self.mode_label.setText("Режим: " + self.sender().text())

    def _start_game(self, settings):
        if self.router['game_window']:
            self.hide()
            self.router['game_window'].set_settings(settings)
            self.router['game_window'].show_game_window()

    def _check_scroll(self, value):
        if value == self.scroll_area.verticalScrollBar().maximum():
            self.button_start_game.setEnabled(True)  # Активируем кнопку
            self.button_start_game.setStyleSheet("QPushButton:hover {background-color: #45a049}")
        else:
            self.button_start_game.setEnabled(False)  # Деактивируем кнопку
            self.button_start_game.setStyleSheet("background-color: #A9A9A9")

    def __init__(self, settings):
        super(MainWindow, self).__init__()
        self.router = {}
        self._settings = settings  # Длина партии в секундах

        self.setWindowTitle("Prisoners dilemma")
        self.setFixedSize(800, 800)
        self.setWindowIcon(QIcon("./images/icon.png"))  # Убедитесь, что файл существует

        # Создаем центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        # Добавляем инструкцию
        self.instructions = QLabel(menu_pages_data[1], self)
        self.instructions.setStyleSheet(styles['common_text_style'])  # Пример стиля
        self.instructions.setWordWrap(True)

        # Создаем виджет для текста
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.addWidget(self.instructions)
        text_widget.setLayout(text_layout)

        # Добавляем скролл
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(text_widget)  # Устанавливаем виджет с текстом в QScrollArea

        layout.addWidget(self.scroll_area)

        # Добавляем кнопку "Начать игру"
        self.button_start_game = QPushButton("Начать игру", self)
        self.button_start_game.setEnabled(False)
        self.button_start_game.setStyleSheet("background-color: #A9A9A9")

        self.button_start_game.clicked.connect(
            lambda: self._start_game(self._settings))
        layout.addWidget(self.button_start_game)

        # Добавляем кнопку обе игры с одним и тем же игроком
        self.button_play_2_with_computer = QPushButton(
            game_mode[0], self)
        self.button_play_2_with_computer.setStyleSheet("pressed: #45a049")
        self.button_play_2_with_computer.clicked.connect(
            lambda: self._on_choice_button_click(0))
        layout.addWidget(self.button_play_2_with_computer)

        # Добавляем кнопку играть вторую партию с игроком АА
        self.button_play_second_with_aa = QPushButton(
            game_mode[1], self)
        self.button_play_second_with_aa.clicked.connect(
            lambda: self._on_choice_button_click(1))
        layout.addWidget(self.button_play_second_with_aa)

        # Добавляем кнопку играть вторую партию с игроком BB
        self.button_play_second_with_bb = QPushButton(
            game_mode[2], self)
        self.button_play_second_with_bb.clicked.connect(
            lambda: self._on_choice_button_click(2))
        layout.addWidget(self.button_play_second_with_bb)

        # Подключаем проверку прокрутки
        self.scroll_area.verticalScrollBar().valueChanged.connect(self._check_scroll)

        self.mode_label = QLabel("Режим: Игра в 2-х партиях с одним и тем же Игроком 2, которого выбирает компьютер",
                                 self)
        self.mode_label.setStyleSheet(styles['mode_label_style'])
        layout.addWidget(self.mode_label)
