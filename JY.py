from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5.Qt import QApplication,qApp
from PyQt5.QtGui import QPixmap
import serial
import serial.tools.list_ports
import port_connection
import sys
import Ui_JY1_newset
import tcp_connection




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
        self.btn_connect_port.clicked.connect(self.port_connection)
        self.btn_disconnect_port.clicked.connect(self.port_close)
        self.btn_city_on.clicked.connect(self.btn_city_on_cb)
        self.btn_city_off.clicked.connect(self.btn_city_off_cb)

       

    def port_check(self):
        self.comboBox_port.clear()
        com = serial.Serial()
        coms_s = {}
        com_list = serial.tools.list_ports.comports()
        
        if len(com_list) <= 0 :
            QMessageBox.critical(self,'错误','无可用端口')
        else:
            for coms in com_list:
                coms_s['%s'%coms[0]] = '%s'%coms[1]
                self.comboBox_port.addItem(coms[0])
        com.close()
            
      

    def port_connection(self):
        self.baud = int(self.comboBox_baud.currentText())
        self.parity = self.comboBox_parity.currentText()
        if self.parity == '无':
            self.parity = 'N'
        if self.parity == '奇校验':
            self.parity = 'O'
        if self.parity == '偶校验':
            self.parity = 'E'
        self.data = int(self.comboBox_byte.currentText())
        self.stop = int(self.comboBox_stop.currentText())
        self.port = self.comboBox_port.currentText()
        self.port_connect.connect(self.port,self.baud,self.parity,self.data,self.stop)
        if self.port_connect.ser.isOpen():
            QMessageBox.warning(self,'提示','%s串口已打开'%self.port)
            self.tabWidget.setEnabled(True)
            self.btn_checkport.setEnabled(False)
            self.btn_connect_port.setEnabled(False)
            self.groupBox_2.setEnabled(False)
            self.port_signal.setPixmap(QPixmap('./image/green_pic.png'))
            self.manger_signal.setPixmap(QPixmap('./image/green_pic.png'))          


    def port_close(self):
        self.port_connect.disconnect()
        if self.port_connect.ser.isOpen() == 0:
            self.tabWidget.setEnabled(False)
            self.btn_checkport.setEnabled(True)
            self.btn_connect_port.setEnabled(True)
            self.groupBox_2.setEnabled(True)
            self.port_signal.setPixmap(QPixmap('./image/red_pic.png'))
            self.manger_signal.setPixmap(QPixmap('./image/red_pic.png'))

    def btn_city_on_cb(self):
        msg = 'AABBCCDDEEFF'
        self.port_connect.send_msg(msg)

        self.city_power_p_val.setText('5000')
        self.city_power_q_val.setText('3000')
        self.city_voltage_val.setText('300')
        self.city_current_val.setText('200')

    def btn_city_off_cb(self):
        self.city_current_val.clear()
        self.city_voltage_val.clear()
        self.city_power_p_val.clear()
        self.city_power_q_val.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = JY_Main()
    win.show()
    sys.exit(app.exec_())
