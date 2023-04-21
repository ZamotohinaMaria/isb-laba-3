import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as as_padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import os
import random


def gen_keys(file_settings: dict, keys: list):
    len_key = random.randint(0, len(keys) - 1)
    key = os.urandom(keys[len_key])
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
    
    with open(file_settings['public_key'], 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))

    with open(file_settings['private_key'], 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()))
            
    with open(file_settings['symmetric_key'], 'wb') as key_file:
        key_file.write(c_key)
    print('\nКлючи сохранены\n')
        
        
def sym_key_decryption(file_settings: dict):
    with open(file_settings['private_key'], 'rb') as file:
        private_bytes = file.read()
    d_private_key = load_pem_private_key(private_bytes,password=None,)

    with open(file_settings['symmetric_key'], 'rb') as file:
        sym_key = file.read()
        
  
    dec_sym_key = d_private_key.decrypt(sym_key,as_padding.OAEP(mgf=as_padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    return dec_sym_key


def text_encryption(file_settings: dict):
    with open(file_settings['initial_file'], 'r', encoding = 'UTF-8') as file:
        text = file.read()
    print('Исходный текст:\n', text)
    
    dec_sym_key = sym_key_decryption(file_settings)
    print('\nКлюч для шифрования получен\n')
    
    padder = sym_padding.ANSIX923(32).padder()
    padded_text = padder.update(bytes(text, 'UTF-8'))+padder.finalize()
    
    cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    enc_text = encryptor.update(padded_text) + encryptor.finalize()
    
    print('\nЗашифрованный текст\n', enc_text)
    
    with open(file_settings['encrypted_file'], 'wb') as file:
        file.write(enc_text)
    
    
def text_decryption(file_settings: dict):
    with open(file_settings['encrypted_file'], 'rb') as file:
        enc_text = file.read()
    
    dec_sym_key = sym_key_decryption(file_settings)
    print('\nКлюч для дешифрки получен\n')
    cipher = Cipher(algorithms.CAST5(dec_sym_key), modes.CBC(iv))
    
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(enc_text) + decryptor.finalize()

    unpadder = sym_padding.ANSIX923(32).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    unpadded_dc_text = unpadded_dc_text.decode('UTF-8')

    print('\nРасшифрованный текст\n', unpadded_dc_text)
    
    
if __name__ == '__main__':
    way = os.path.abspath('')
    file_settings= {
        'initial_file': way + '\\' + 'initial_file.txt',
        'encrypted_file': way + '\\' + 'encrypted_file.txt',
        'decrypted_file': way + '\\' + 'decrypted_file.txt',
        'symmetric_key': way + '\\' + 'symmetric_key.txt',
        'public_key': way + '\\' + 'public_key.pem',
        'private_key': way + '\\' + 'private_key.pem',
    }

    keys = [i for i in range(5, 17, 1)]
    iv = os.urandom(8)
    gen_keys(file_settings, keys)
    text_encryption(file_settings)
    text_decryption(file_settings)