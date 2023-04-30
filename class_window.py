from PyQt5.QtWidgets import (
    QPushButton,
    QMainWindow,
    QLabel,
    QDesktopWidget)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5 import QtCore
from class_encryptor import Encryptor as enc
from enum import Enum

flag = 0

class Window(QMainWindow):
    def __init__(self) -> None:
        """функция инициализации
        """
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        """функция работы окна
        """
        self.enc = enc()     
        self.info_message = QLabel(self)
        self.btn_gen_keys = QPushButton('Сгенерировать ключи', self)
        self.btn_enc_txt = QPushButton('Зашифровать текст', self)
        self.btn_dec_txt = QPushButton('Дешифровать текст', self)

        self.settings()
        
        self.setFixedWidth(self.w)
        self.setFixedHeight(self.h)
        self.center()
        self.setWindowTitle('OIB laba 3')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('background-color: #dbdcff;')
        self.show()

    def settings(self) -> None:
        """функция настройки элементов графического интерфейса
        """
        self.w = 900
        self.h = 500
        self.info_message.resize(self.w, self.h)
        self.info_message.setFont(QFont('Arial', 12))
        self.info_message.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_x_size = 300
        self.btn_y_size = 40
        self.luft = 0
        self.btn_font_main = QFont('Arial', 11)
        self.btn_StyleSheet_main = 'background-color: #171982; color: #dbdcff; border :1px solid;'

        self.btn_gen_keys.setGeometry(
            self.luft, 0, self.btn_x_size, self.btn_y_size)
        self.btn_gen_keys.setFont(self.btn_font_main)
        self.btn_gen_keys.setStyleSheet(self.btn_StyleSheet_main)
        self.btn_gen_keys.clicked.connect(self.gen_keys)

        self.btn_enc_txt.setGeometry(self.btn_x_size + self.luft + 5, 0,
                                     self.btn_x_size, self.btn_y_size)
        self.btn_enc_txt.setFont(self.btn_font_main)
        self.btn_enc_txt.setStyleSheet(self.btn_StyleSheet_main)
        self.btn_enc_txt.clicked.connect(self.text_encryption)

        self.btn_dec_txt.setGeometry(2 * self.btn_x_size + self.luft + 10, 0,
                                     self.btn_x_size, self.btn_y_size)
        self.btn_dec_txt.setFont(self.btn_font_main)
        self.btn_dec_txt.setStyleSheet(self.btn_StyleSheet_main)
        self.btn_dec_txt.clicked.connect(self.text_decryption)

    def center(self) -> None:
        """функция централизации окна на экране
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def print_info_message(self, text: str) -> None:
        """функция вывода информации об этапах работы программы
        и ошибках

        Args:
            text (str): выводимое сообщение
        """
        self.info_message.clear()
        self.info_message.setText(text)
        self.info_message.show()

    def gen_keys(self) -> None:
        """функция работы кнопки для генерации ключей
        """
        flag = self.enc.gen_keys()
        if (flag == 0):
            self.print_info_message(
                'Ключи шифрования сгенерированы и записаны в файлы')
        elif (flag == 1):
            self.print_info_message(
                'Ошибка доступа к файлу при генерации ключей')

    def text_encryption(self) -> None:
        """функция работы кнопки для шифрования текста
        """
        flag = self.enc.text_encryption()
        if (flag == 0):
            self.print_info_message(
                'Текст зашифрован и записан в файл')
        elif (flag == 1):
            self.print_info_message(
                'Ошибка доступа к файлу с исходным текстом')
        elif (flag == 3):
            self.print_info_message('Ошибка доступа к файлам с ключами')
        elif (flag == 4):
            self.print_info_message(
                'Ошибка доступа к файлу с вектором шифрования')

    def text_decryption(self) -> None:
        """функция работы кнопки для расшифровки текста
        """
        flag = self.enc.text_decryption()
        if(flag == 0):
            self.print_info_message(
                'Текст расшифрован и записан в файл')
        elif (flag == 2):
            self.print_info_message(
                'Ошибка доступа к файлу с зашифрованным текстом')
        elif (flag == 3):
            self.print_info_message('Ошибка доступа к файлам с ключами')
        elif (flag == 3):
            self.print_info_message(
                'Ошибка доступа к файлу с вектором шифрования')
