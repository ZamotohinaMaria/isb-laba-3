from cryptography.hazmat.primitives import (serialization, hashes, padding as sym_padding)
from cryptography.hazmat.primitives.asymmetric import (rsa, padding as as_padding)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import sys
from PyQt5.QtWidgets import ( QPushButton, QApplication, QMainWindow, QLabel)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5 import QtCore
import os
import random
import time


    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI() 
    
    def initUI(self):
        self.way = os.path.abspath('')
        self.file_settings= {
            'initial_file': self.way + '\\' + 'initial_file.txt',
            'encrypted_file': self.way + '\\' + 'encrypted_file.txt',
            'decrypted_file': self.way + '\\' + 'decrypted_file.txt',
            'symmetric_key': self.way + '\\' + 'symmetric_key.txt',
            'public_key': self.way + '\\' + 'public_key.pem',
            'private_key': self.way + '\\' + 'private_key.pem',
        }

        self.keys = [i for i in range(5, 17, 1)]
        self.iv = os.urandom(8)
        self.info_message = QLabel(self)
        self.info_message.resize(1200, 50)
        self.info_message.move(0, 70)
        self.info_message.setFont(QFont('Arial', 14))
        self.info_message.setAlignment(QtCore.Qt.AlignCenter)
        self.flag = 0
        
        self.btn_x_size = 300
        self.btn_y_size = 40
        self.lust = 140
        btn_font_main = QFont('Arial', 11)
        btn_StyleSheet_main = 'background-color: #171982; color: #dbdcff; border :1px solid; '

        #-------------------------------------------------------------------------------------------------------
        self.btn_gen_keys = QPushButton('Сгенерировать ключи', self)
        self.btn_gen_keys.setGeometry(self.lust, 0, self.btn_x_size, self.btn_y_size)
        self.btn_gen_keys.setFont(btn_font_main)
        self.btn_gen_keys.setStyleSheet(btn_StyleSheet_main)
        self.btn_gen_keys.clicked.connect(self.gen_keys)
        #-------------------------------------------------------------------------------------------------------
        self.btn_enc_txt = QPushButton('Зашифровать текст', self)
        self.btn_enc_txt.setGeometry(self.btn_x_size + self.lust + 5, 0, self.btn_x_size, self.btn_y_size)
        self.btn_enc_txt.setFont(btn_font_main)
        self.btn_enc_txt.setStyleSheet(btn_StyleSheet_main)
        self.btn_enc_txt.clicked.connect(self.text_encryption)
        #-------------------------------------------------------------------------------------------------------
        self.btn_dec_txt = QPushButton('Дешифровать текст', self)
        self.btn_dec_txt.setGeometry(2*self.btn_x_size + self.lust + 10, 0, self.btn_x_size, self.btn_y_size)
        self.btn_dec_txt.setFont(btn_font_main)
        self.btn_dec_txt.setStyleSheet(btn_StyleSheet_main)
        self.btn_dec_txt.clicked.connect(self.text_decryption)
        #-------------------------------------------------------------------------------------------------------

        #упраление окошком
        self.setGeometry(50, 50, 1200, 675)
        self.setWindowTitle('Application programing laba 3')
        self.setWindowIcon(QIcon('web.png'))
        self.setStyleSheet('background-color: #dbdcff;')
        self.show()
    
    def print_text(self, text):
        self.info_message.clear()
        self.info_message.setText(text)
        self.info_message.show()
        
    
    def gen_keys(self):
        if (self.flag == 0):
            len_key = random.randint(0, len(self.keys) - 1)
            key = os.urandom(self.keys[len_key])
            print('\nСгенерирован ключ симетричного шифрования\n')


            assym_keys = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            private_key = assym_keys
            print('\nСгенерирован закрытый ключ ассиметричного шифрования\n')
            public_key = assym_keys.public_key()
            print('\nСгенерирован открытый ключ ассиметричного шифрования\n')
            
            c_key = public_key.encrypt(key, as_padding.OAEP(mgf=as_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
            print('\nКлюч симметричного шифрования зашифрован\n')
            
            with open(self.file_settings['public_key'], 'wb') as public_out:
                    public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo))

            with open(self.file_settings['private_key'], 'wb') as private_out:
                    private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()))
                    
            with open(self.file_settings['symmetric_key'], 'wb') as key_file:
                key_file.write(c_key)
            print('\nКлючи сохранены\n')
            self.print_text('Ключи шифрования сгенерированы и записаны в файлы')
            self.flag = 1
        else:
            self.print_text('Ключи уже сгенерированы')
            
            
    def sym_key_decryption(self):
        with open(self.file_settings['private_key'], 'rb') as file:
            private_bytes = file.read()
        d_private_key = load_pem_private_key(private_bytes,password=None,)

        with open(self.file_settings['symmetric_key'], 'rb') as file:
            sym_key = file.read()
            
        dec_sym_key = d_private_key.decrypt(sym_key,as_padding.OAEP(mgf=as_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        
        return dec_sym_key


    def text_encryption(self):
        if(self.flag == 1 or self.flag == 2):
            with open(self.file_settings['initial_file'], 'r', encoding = 'UTF-8') as file:
                text = file.read()
            print('Исходный текст:\n', text)
            
            dec_sym_key = self.sym_key_decryption()
            print('\nКлюч для шифрования получен\n')
            
            padder = sym_padding.ANSIX923(32).padder()
            padded_text = padder.update(bytes(text, 'UTF-8'))+padder.finalize()
            
            cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(self.iv))
            encryptor = cipher.encryptor()
            enc_text = encryptor.update(padded_text) + encryptor.finalize()
            
            print('\nЗашифрованный текст\n', enc_text)
            
            with open(self.file_settings['encrypted_file'], 'wb') as file:
                file.write(enc_text)
            self.print_text('Текст зашифрован и записан в файл')
            self.flag = 2
        elif (self.flag == 0):
            self.print_text('Сначала сгенерируйте ключи')
        
        
    def text_decryption(self):
        if(self.flag == 2):
            with open(self.file_settings['encrypted_file'], 'rb') as file:
                enc_text = file.read()
            
            dec_sym_key = self.sym_key_decryption()
            print('\nКлюч для дешифрки получен\n')
            cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(self.iv))
            
            decryptor = cipher.decryptor()
            dc_text = decryptor.update(enc_text) + decryptor.finalize()

            unpadder = sym_padding.ANSIX923(32).unpadder()
            unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
            unpadded_dc_text = unpadded_dc_text.decode('UTF-8')

            print('\nРасшифрованный текст\n', unpadded_dc_text)
            
            with open(self.file_settings['decrypted_file'], 'wb') as file:
                file.write(enc_text)
            self.print_text('Текст расшифрован и записан в файл')
            self.flag = 0
        elif (self.flag == 0):
            self.print_text('Сначала сгенерируйте ключи')
        elif (self.flag == 1):
            self.print_text('Сначала зашифруйте текст')

if __name__ == '__main__':
    app = QApplication(sys.argv) #объект приложение, должен быть всегда, принимает на вход аргументы командной строки
    ex = Window()
    sys.exit(app.exec_())
    
    
    