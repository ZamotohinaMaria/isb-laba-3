from PyQt5.QtWidgets import (
    QPushButton,
    QMainWindow,
    QLabel,
    QDesktopWidget, 
    QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5 import QtCore
from class_encryptor import encryptor as enc

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self): 
        self.enc = enc()
        self.flag = 0
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

    def settings(self):        
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
    
    def gen_keys(self):
        if self.flag == 0:
            self.enc.gen_keys()
            self.print_info_message(
                'Ключи шифрования сгенерированы и записаны в файлы')
            self.flag = 1
        else:
            self.print_info_message('Ключи уже сгенерированы')
            
    def text_encryption(self):
        if (self.flag == 1 or self.flag == 2):
            self.enc.text_encryption()
            self.print_info_message(
                'Текст зашифрован и записан в файл')
            self.flag = 2
        elif (self.flag == 0):
            self.print_info_message('Сначала сгенерируйте ключи')
            
    def text_decryption(self):
        if(self.flag == 2):
            self.enc.text_decryption()
            self.print_info_message(
                'Текст расшифрован и записан в файл')
            self.flag = 0
        elif (self.flag == 0):
            self.print_info_message('Сначала сгенерируйте ключи')
        elif (self.flag == 1):
            self.print_info_message('Сначала зашифруйте текст')
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def print_info_message(self, text):
        self.info_message.clear()
        self.info_message.setText(text)
        self.info_message.show()