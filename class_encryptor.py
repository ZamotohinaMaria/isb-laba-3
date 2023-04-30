from cryptography.hazmat.primitives import (
    serialization, hashes, padding as sym_padding)
from cryptography.hazmat.primitives.asymmetric import (
    rsa, padding as as_padding)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from PyQt5.QtWidgets import (QMainWindow, QFileDialog)
import os
import random
from enum import Enum
import logging
        

class Flag(Enum):
    file_error_text = 1
    file_error_enc_text = 2
    file_error_keys = 3
    file_error_enc_vec = 4
    file_good = 0


class Encryptor():
    def __init__(self) -> None:
        """функция инициализации
        """
        self.way_to_init_text = str(QFileDialog.getOpenFileName(caption='Select file for encrypt', filter='*.txt'))
        self.way_to_init_text = self.way_to_init_text.split('\'')[1]
        self.way = str(QFileDialog.getExistingDirectory(caption='Select folder for dataset'))
        self.flag = Flag
        self.file_settings = {
            'initial_file': self.way_to_init_text,
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'symmetric_key': os.path.join(self.way, 'symmetric_key.txt'),
            'public_key': os.path.join(self.way, 'public_key.txt'),
            'private_key': os.path.join(self.way, 'private_key.txt'),
            'encrypted_vector': os.path.join(self.way, 'encrypted_vector.txt')
        }

        self.keys = [i for i in range(5, 17, 1)]
        
    def gen_keys(self) -> Flag:
        """функция генерации ключей для симмтричного и асиметричного шифрования

        Returns:
            Flag: индикатор работы с файлами
        """
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
        try: 
            with open(self.file_settings['public_key'], 'wb') as public_out:
                public_out.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except IOError:
            logging.error(f"error in file {self.file_settings['public_key']}")
        else:
            logging.info('public key is created and written to the file')
            
        try:
            with open(self.file_settings['private_key'], 'wb') as private_out:
                private_out.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()))
        except IOError:
            logging.error(f"error in file {self.file_settings['private_key']}")
        else:
            logging.info('private key is created and written to the file')

        try:
            with open(self.file_settings['symmetric_key'], 'wb') as key_file:
                key_file.write(c_key)
        except IOError:
            logging.error(f"error in file {self.file_settings['symmetric_key']}")
        else:
            logging.info('symmetric key is created and written to the file')

        iv = os.urandom(8)
        try:
            with open(self.file_settings['encrypted_vector'], 'wb') as enc_vec:
                enc_vec.write(iv)
        except IOError:
            logging.error(f"error in file {self.file_settings['encrypted_vector']}")
        else:
            logging.info('encrypted vector is created and written to the file')

        return self.flag.file_good.value

    def sym_key_decryption(self) -> bytes or Flag:
        """функция доступа и расшифровки ключа симметричного шифрования

        Returns:
            bytes | Flag: при удачной работе с файлами возврщает ключ
            симметричного шифрования
            при ошибке возвращает индиктар ошибки
        """
        if (os.path.isfile(self.file_settings['private_key']) == False):
            return self.flag.file_error_keys.value
        else:
            try:
                with open(self.file_settings['private_key'], 'rb') as file:
                    private_bytes = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['private_key']}")

        d_private_key = load_pem_private_key(private_bytes, password=None,)

        if (os.path.isfile(self.file_settings['symmetric_key']) == False):
            return self.flag.file_error_keys.value
        else:
            try:
                with open(self.file_settings['symmetric_key'], 'rb') as file:
                    sym_key = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['symmetric_key']}")

        dec_sym_key = d_private_key.decrypt(
            sym_key,
            as_padding.OAEP(
                mgf=as_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))

        return dec_sym_key

    def text_encryption(self) -> Flag:
        """функция зашифровки текста алгоритмом CAST5

        Returns:
            Flag: индикатор работы с файлами
        """
        if (os.path.isfile(self.file_settings['initial_file']) == False):
            return self.flag.file_error_text.value
        else:
            try:
                with open(self.file_settings['initial_file'], 'r', encoding='UTF-8') as file:
                    text = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['initial_file']}")

        if (os.path.isfile(self.file_settings['encrypted_vector']) == False):
            return self.flag.file_error_enc_vec.value
        else:
            try:
                with open(self.file_settings['encrypted_vector'], 'rb') as file:
                    iv = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['encrypted_vector']}")

        if (self.sym_key_decryption() == 3):
            return self.flag.file_error_keys.value
        else:
            dec_sym_key = self.sym_key_decryption()

        padder = sym_padding.ANSIX923(32).padder()
        padded_text = padder.update(
            bytes(text, 'UTF-8')) + padder.finalize()

        cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        enc_text = encryptor.update(padded_text) + encryptor.finalize()

        try:
            with open(self.file_settings['encrypted_file'], 'wb') as file:
                file.write(enc_text)
        except IOError:
            logging.error(f"error in file {self.file_settings['encrypted_file']}")
        else:
            logging.info('text is encrypted and written to the file')

        return self.flag.file_good.value

    def text_decryption(self) -> Flag:
        """функция расшифровки текста алгоритмом CAST5

        Returns:
            Flag: индикатор работы с файлами
        """
        if (os.path.isfile(self.file_settings['encrypted_file']) == False):
            return self.flag.file_error_enc_text.value
        else:
            try:
                with open(self.file_settings['encrypted_file'], 'rb') as file:
                    enc_text = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['encrypted_file']}")

        if (os.path.isfile(self.file_settings['encrypted_vector']) == False):
            return self.flag.file_error_enc_vec.value
        else:
            try:
                with open(self.file_settings['encrypted_vector'], 'rb') as file:
                    iv = file.read()
            except IOError:
                logging.error(f"error in file {self.file_settings['encrypted_vector']}")

        if (self.sym_key_decryption() == 3):
            return self.flag.file_error_keys.value
        else:
            dec_sym_key = self.sym_key_decryption()

        cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))

        decryptor = cipher.decryptor()
        dc_text = decryptor.update(enc_text) + decryptor.finalize()

        unpadder = sym_padding.ANSIX923(32).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        unpadded_dc_text = unpadded_dc_text.decode('UTF-8')

        try:
            with open(self.file_settings['decrypted_file'], 'w') as file:
                file.write(unpadded_dc_text)
        except IOError:
                logging.error(f"error in file {self.file_settings['decrypted_file']}")
        else:
            logging.info('text is decrypted and written to the file')

        return self.flag.file_good.value
