from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QApplication,qApp
# from PyQt5.QtCore import qApp
import sys
import Ui_JY1_newset



class JY_Main(QMainWindow,Ui_JY1_newset.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('JY1_test')
        with open("style.qss", 'r') as f:
            qApp.setStyleSheet(f.read())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = JY_Main()
    win.show()
    sys.exit(app.exec_())
