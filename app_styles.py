app_styles = """
            QWidget {
                background-color: #E0FFFF;
                }
            QLabel {
                font-size: 26px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #E0FFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                font-size: 20px;  
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QScrollBar:vertical {
                border: 2px solid #888; /* Цвет границы */
                background: #f0f0f0; /* Цвет фона */
                width: 20px; /* Увеличиваем ширину скролла */
                margin: 20px 0 20px 0; /* Отступы */
            }
            QScrollBar::handle:vertical {
                background: #3CB371; /* Цвет ползунка */
                min-height: 20px; /* Увеличиваем минимальную высоту ползунка */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none; /* Убираем фон для кнопок */
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none; /* Убираем фон для страниц */
            }
            QScrollBar:horizontal {
                border: 2px solid #888; /* Цвет границы */
                background: #f0f0f0; /* Цвет фона */
                height: 20px; /* Увеличиваем высоту скролла */
                margin: 0 22px 0 22px; /* Отступы */
            }
            QScrollBar::handle:horizontal {
                background: #d2051e; /* Цвет ползунка */
                min-width: 10px; /* Увеличиваем минимальную ширину ползунка */
            }  
            QMessageBox QPushButton {
                color: white; 
                background-color: #4CAF50; 
                border-radius: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
            QMessageBox QLabel {
                color: #45a049;
                font-size: 20px;
            }
            
        """