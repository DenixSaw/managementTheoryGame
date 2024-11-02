from time import sleep
from random import randint, uniform
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, \
    QSizePolicy, QMessageBox

import settings
from data.text_data import styles


# Окно GameWindow предназначено для одной партии с определенным переданным settings - настройкой начальных параметров партии
class GameWindow(QMainWindow):

    def set_settings(self, settings):
        self._settings = settings

    def set_router(self, router):
        self._router = router

    def print_router(self):
        print(self._router)

    def _choice_buttons_enabled(self):
        self.button_0.setEnabled(True)
        self.button_1.setEnabled(True)
        self.button_0.setStyleSheet("QPushButton:hover {background-color: #45a049}")
        self.button_1.setStyleSheet("QPushButton:hover {background-color: #45a049}")

    def _start_game(self):
        print(self._settings)

        self.label_num_of_rounds.setText(f"Партия № {self._settings['round']}")
        self.label_player_1_score.setText(f"{self._settings['player_1_score']}")
        self.label_player_2_score.setText(f"{self._settings['player_2_score']}")
        self.label_timer.setText(f"Время от начала партии Ожидаем Игрока 2")
        self.log_text_label.setText(" ")
        self._choice_buttons_enabled()
        self.time_counter = 0
        sleep(0.48)  # TODO: Сделать лучше? Эта хрень просто тормозит всю прогу
        self._start_timer()

    def _check_winner_in_round(self):
        message_box = QMessageBox()
        message_box.setFixedSize(250, 250)
        message_text = ""

        message_box.setWindowTitle('Партия окончена')
        if self._settings['player_1_score'] > self._settings['player_2_score']:
            message_text = message_text + 'Вы выйграли!'
        elif self._settings['player_1_score'] < self._settings['player_2_score']:
            message_text = message_text + 'Выйграл игрок 2!'
        else:
            message_text = message_text + 'Ничья!'

        if self._settings['round'] == 1:
            message_text = message_text + '\n' + 'Если вы готовы ко второй партии нажмите "Ок" '
        message_box.setText(message_text)

        try:
            file_with_stats = open('statistic.txt', 'a', encoding='utf-8')
            file_with_stats.writelines("\n".join(self._statistic))
            file_with_stats.write('\n\n')
            file_with_stats.close()
            self._statistic.clear()
        except Exception as e:
            print(e)
        response = message_box.exec()

        if response == QMessageBox.StandardButton.Ok and self._settings['round'] != 2:
            self._settings['round'] += 1
            self._settings['player_1_score'] = 0
            self._settings['player_2_score'] = 0
            self._start_game()
        elif response == QMessageBox.StandardButton.Ok and self._settings['round'] == 2:
            for item in self._router.values():
                item.close()

    def _check_winner_in_turn(self):
        self.choice_player_1 = self.sender().text()

        rand = uniform(0.0, 1.0)

        # Посчитано какое зачение присвоить выбору Игрока 2
        print(rand)
        if rand < self._settings['0']:
            self.choice_player_2 = '0'
        else:
            self.choice_player_2 = '1'

        delay_timer = QTimer(self)
        rand_time = 1000  # randint(5000, 10000)
        self.delay = True

        self.button_0.setEnabled(False)
        self.button_1.setEnabled(False)
        self.button_0.setStyleSheet("background-color: #A9A9A9")
        self.button_1.setStyleSheet("background-color: #A9A9A9")

        def delay_to_false():
            self.delay = False

            # print('Вышел из задержки')
            # Здесь начисляем выигрыш
            if self.choice_player_2 == self.choice_player_1 == '1':
                self._settings['player_1_score'] += 100
                self._settings['player_2_score'] += 100
            elif self.choice_player_1 == '0' and self.choice_player_2 == '1':
                self._settings['player_1_score'] += 500
            elif self.choice_player_1 == '1' and self.choice_player_2 == '0':
                self._settings['player_2_score'] += 500

            # print(self._settings)
            # Обновляем счет на экране
            self.label_player_1_score.setText(f"{self._settings['player_1_score']}")
            self.label_player_2_score.setText(f"{self._settings['player_2_score']}")
            # Разблокируем кнопки

            if not self._time_is_left:
                self._choice_buttons_enabled()
            self.log_text = f'Вы выбрали:{self.choice_player_1} | Игрок 2 выбрал:{self.choice_player_2}'  # f'Вы выбрали:{self.choice_player_1} | Игрок 2 выбрал:{self.choice_player_2}\n{self.log_text}'

            self._statistic.append(
                f'П{self._settings['round']} | И1: {self.choice_player_1} | И2: {self.choice_player_2} | Счет И1: {self._settings['player_1_score']} | Счет И2: {self._settings['player_2_score']}')

            self.log_text_label.setText(self.log_text)
            if self._time_is_left:
                self._check_winner_in_round()

        delay_timer.setSingleShot(True)
        delay_timer.timeout.connect(delay_to_false)
        delay_timer.start(rand_time)

    def show_game_window(self):
        self.show()
        self._start_game()

    def __init__(self, router: dict = None, settings: dict = settings.default_settings):
        super().__init__()
        self._router = router
        self._settings = settings
        self.log_text = ""
        self._time_is_left = False
        self._statistic = []

        self.setWindowTitle("Prisoners dilemma")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("./images/icon.png"))

        # Создаем центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный макет
        main_layout = QVBoxLayout(central_widget)

        game_info_layout = QHBoxLayout()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.time_counter = 0  # Счетчик времени

        # Номер партии. Надпись
        self.label_num_of_rounds = QLabel()
        self.label_num_of_rounds.setStyleSheet(styles['common_text_style'])
        game_info_layout.addWidget(self.label_num_of_rounds)

        # Таймер партии
        self.label_timer = QLabel()
        self.label_timer.setStyleSheet(styles['common_text_style'])
        game_info_layout.addWidget(self.label_timer)

        main_layout.addLayout(game_info_layout)

        # Добавляем счет игроков

        # Игрок 1
        player_layout = QHBoxLayout()
        self.label_player_1 = QLabel("Игрок 1 (Вы):", self)
        self.label_player_1.setStyleSheet(styles['common_text_style'])
        player_layout.addWidget(self.label_player_1)

        self.label_player_1_score = QLabel()
        self.label_player_1_score.setStyleSheet(styles['common_text_style'])
        player_layout.addWidget(self.label_player_1_score)

        # Игрок 2
        self.label_player_2 = QLabel("Игрок 2:", self)
        self.label_player_2.setStyleSheet(styles['common_text_style'])
        player_layout.addWidget(self.label_player_2)

        self.label_player_2_score = QLabel()
        self.label_player_2_score.setStyleSheet(styles['common_text_style'])
        player_layout.addWidget(self.label_player_2_score)

        main_layout.addLayout(player_layout)

        self.log_layout = QVBoxLayout()
        self.log_label = QLabel("Журнал:")
        self.log_label.setStyleSheet(styles['common_text_style'])
        self.log_layout.addWidget(self.log_label)
        main_layout.addLayout(self.log_layout)

        self.log_text_label = QLabel(self.log_text, self)
        self.log_text_label.setStyleSheet(styles['common_text_style'])  # Пример стиля
        self.log_text_label.setWordWrap(True)
        self.log_text_label.setMinimumHeight(390)
        self.log_text_label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                          QSizePolicy.Policy.Minimum)  # Устанавливаем политику размера
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.addWidget(self.log_text_label)
        text_widget.setLayout(text_layout)

        # Добавляем скролл
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(text_widget)  # Устанавливаем виджет с текстом в QScrollArea
        self.scroll_area.setMinimumHeight(420)
        main_layout.addWidget(self.scroll_area)

        # Добавляем кнопки для Игрока 1
        main_layout.addStretch(1)  # Это чтобы кнопки были внизу экрана
        # Добавляем кнопки "0" и "1"
        button_layout = QHBoxLayout()

        self.button_0 = QPushButton("0", self)
        button_layout.addWidget(self.button_0)
        self.button_0.clicked.connect(self._check_winner_in_turn)

        self.button_1 = QPushButton("1", self)
        button_layout.addWidget(self.button_1)
        self.button_1.clicked.connect(self._check_winner_in_turn)
        main_layout.addLayout(button_layout)

    # В 25 минутах 1500 секунд
    def _start_timer(self):
        self._time_is_left = False
        self.timer.start(1000)  # Запускаем таймер с интервалом 1000 мс (1 секунда)

    def _stop_timer(self):
        self.timer.stop()  # Останавливаем таймер
        self._time_is_left = True
        # print('Timer stopped')

    def _update_timer(self):
        self.time_counter += 1  # Увеличиваем счетчик
        minutes = self.time_counter // 60  # Вычисляем минуты
        seconds = self.time_counter % 60  # Вычисляем секунды
        self.label_timer.setText(
            f"Время от начала партии {minutes:02}:{seconds:02}")  # Обновляем текст метки в формате ММ:СС
        if self.time_counter == self._settings['game_length']:
            self._stop_timer()
