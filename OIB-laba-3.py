import sys
from PyQt5.QtWidgets import (QApplication)
from class_window import Window
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w')
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
