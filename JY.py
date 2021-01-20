from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QApplication,qApp
import port_connection
import sys
import Ui_JY1_newset



class JY_Main(QMainWindow,Ui_JY1_newset.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('JY1_test')
        with open("style.qss", 'r') as f:
            qApp.setStyleSheet(f.read())

        self.port_connect = port_connection.port_connect()
        self.tabWidget.setEnabled(False)
        self.btn_checkport.clicked.connect(self.port_check)
       

    def port_check(self):
        self.baud = self.comboBox_baud.currentText()
        self.parity = self.comboBox_parity.currentText()
        self.data = self.comboBox_byte.currentText()
        self.stop = self.comboBox_stop.currentText()
        self.port = self.port_connect.check()
        self.comboBox_port.addItem(self.port)

    def port_connect(self):

        self.tabWidget.setEnabled(True)
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = JY_Main()
    win.show()
    sys.exit(app.exec_())
