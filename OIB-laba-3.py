from cryptography.hazmat.primitives import (
    serialization, hashes, padding as sym_padding)
from cryptography.hazmat.primitives.asymmetric import (
    rsa, padding as as_padding)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import sys
from PyQt5.QtWidgets import (
    QPushButton,
    QApplication,
    QMainWindow,
    QLabel,
    QDesktopWidget, 
    QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5 import QtCore
import os
import random


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  
        # self.init_text = str(QFileDialog.getOpenFileName(self, 'Select file for encrypt', '*.txt'))
        # self.way = str(QFileDialog.getExistingDirectory(self, 'Select folder for dataset'))
        self.way = os.path.abspath('')
             
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
        self.file_settings = {
            'initial_file': os.path.join(self.way, 'initial_file.txt'),
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'symmetric_key': os.path.join(self.way, 'symmetric_key.txt'),
            'public_key': os.path.join(self.way, 'public_key.txt'),
            'private_key': os.path.join(self.way, 'private_key.txt'),
            'encrypted_vector': os.path.join(self.way, 'encrypted_vector.txt')
        }

        self.keys = [i for i in range(5, 17, 1)]
        self.flag = 0
        
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
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def print_info_message(self, text):
        self.info_message.clear()
        self.info_message.setText(text)
        self.info_message.show()

    def gen_keys(self):
        if (self.flag == 0):
            len_key = random.randint(0, len(self.keys) - 1)
            sym_key = os.urandom(self.keys[len_key])

            assym_keys = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            private_key = assym_keys
            public_key = assym_keys.public_key()

            c_key = public_key.encrypt(
                sym_key,
                as_padding.OAEP(
                    mgf=as_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None))

            with open(self.file_settings['public_key'], 'wb') as public_out:
                public_out.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))

            with open(self.file_settings['private_key'], 'wb') as private_out:
                private_out.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))

            with open(self.file_settings['symmetric_key'], 'wb') as key_file:
                key_file.write(c_key)
                
            iv = os.urandom(8)
            with open(self.file_settings['encrypted_vector'], 'wb') as enc_vec:
                enc_vec.write(iv)
                
            self.print_info_message(
                'Ключи шифрования сгенерированы и записаны в файлы')
            self.flag = 1
        else:
            self.print_info_message('Ключи уже сгенерированы')

    def sym_key_decryption(self):
        with open(self.file_settings['private_key'], 'rb') as file:
            private_bytes = file.read()
        d_private_key = load_pem_private_key(private_bytes, password=None,)

        with open(self.file_settings['symmetric_key'], 'rb') as file:
            sym_key = file.read()

        dec_sym_key = d_private_key.decrypt(
            sym_key,
            as_padding.OAEP(
                mgf=as_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))

        return dec_sym_key

    def text_encryption(self):
        if(self.flag == 1 or self.flag == 2):
            with open(self.file_settings['initial_file'], 'r', encoding='UTF-8') as file:
                text = file.read()
                
            with open(self.file_settings['encrypted_vector'], 'rb') as file:
                iv = file.read()

            dec_sym_key = self.sym_key_decryption()

            padder = sym_padding.ANSIX923(32).padder()
            padded_text = padder.update(
                bytes(text, 'UTF-8')) + padder.finalize()

            cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            enc_text = encryptor.update(padded_text) + encryptor.finalize()

            with open(self.file_settings['encrypted_file'], 'wb') as file:
                file.write(enc_text)
            self.print_info_message(
                'Текст зашифрован и записан в файл')
            self.flag = 2
        elif (self.flag == 0):
            self.print_info_message('Сначала сгенерируйте ключи')

    def text_decryption(self):
        if(self.flag == 2):
            with open(self.file_settings['encrypted_file'], 'rb') as file:
                enc_text = file.read()
                
            with open(self.file_settings['encrypted_vector'], 'rb') as file:
                iv = file.read()

            dec_sym_key = self.sym_key_decryption()
            cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))

            decryptor = cipher.decryptor()
            dc_text = decryptor.update(enc_text) + decryptor.finalize()

            unpadder = sym_padding.ANSIX923(32).unpadder()
            unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
            unpadded_dc_text = unpadded_dc_text.decode('UTF-8')

            with open(self.file_settings['decrypted_file'], 'w') as file:
                file.write(unpadded_dc_text)
            self.print_info_message(
                'Текст расшифрован и записан в файл')
            self.flag = 0
        elif (self.flag == 0):
            self.print_info_message('Сначала сгенерируйте ключи')
        elif (self.flag == 1):
            self.print_info_message('Сначала зашифруйте текст')


if __name__ == '__main__':
    # объект приложение, должен быть всегда, принимает на вход аргументы
    # командной строки
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
