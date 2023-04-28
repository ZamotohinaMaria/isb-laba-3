import sys
from PyQt5.QtWidgets import (QApplication)
from class_window import Window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
