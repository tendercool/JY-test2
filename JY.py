from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.Qt import QApplication, qApp
from PyQt5.QtGui import QPixmap
import serial
import serial.tools.list_ports
import port_connection
import sys
import Ui_JY1_newset
import tcp_connection
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import socket


class JY_Main(QMainWindow, Ui_JY1_newset.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('JY1_test -- by:燊林')
        with open("style.qss", 'r') as f:
            qApp.setStyleSheet(f.read())

        self.bms_val = [
            'bms_val_1', 'bms_val_2', 'bms_val_3', 'bms_val_4', 'bms_val_5',
            'bms_val_6', 'bms_val_7', 'bms_val_8', 'bms_val_9', 'bms_val_10',
            'bms_val_11', 'bms_val_12', 'bms_val_13', 'bms_val_14',
            'bms_val_15', 'bms_val_16', 'bms_val_17', 'bms_val_18',
            'bms_val_19', 'bms_val_20', 'bms_val_21', 'bms_val_22',
            'bms_val_23', 'bms_val_24', 'bms_val_25', 'bms_val_26',
            'bms_val_27'
        ]

        self.pcs_val = [
            'pcs_val_1', 'pcs_val_2', 'pcs_val_3', 'pcs_val_4', 'pcs_val_5',
            'pcs_val_6', 'pcs_val_7', 'pcs_val_8', 'pcs_val_9', 'pcs_val_10',
            'pcs_val_11', 'pcs_val_12', 'pcs_val_13'
        ]

        self.diesel_val = [
            'diesel_val_1', 'diesel_val_2', 'diesel_val_3', 'diesel_val_4',
            'diesel_val_5', 'diesel_val_6', 'diesel_val_7', 'diesel_val_8',
            'diesel_val_9', 'diesel_val_10', 'diesel_val_11', 'diesel_val_12',
            'diesel_val_13', 'diesel_val_14', 'diesel_val_15', 'diesel_val_16'
        ]

        self.tabWidget.setEnabled(False)
        self.btn_checkport.clicked.connect(self.port_check)
        self.btn_connect_port.clicked.connect(self.port_connection)
        self.btn_disconnect_port.clicked.connect(self.port_close)
        self.btn_city_on.clicked.connect(self.btn_city_on_cb)
        self.btn_city_off.setEnabled(False)
        self.btn_city_off.clicked.connect(self.btn_city_off_cb)

        self.btn_tcp_retry.clicked.connect(self.tcp_host)
        self.btn_connect_tcp.clicked.connect(self.tcp_connection)

        self.ctiy_flag = 0
        self.sig_2km_flag = 0
        self.sig_pv_flag = 0
        self.sig_load1_flag = 0
        self.sig_load2_flag = 0
        self.sig_load3_flag = 0
        self.sig_diesel_flag = 0
        self.sig_bms_flag = 0
        self.sig_pcs_flag = 0

        self.btn_disconnect_port.setEnabled(False)
        self.btn_2KM_on.clicked.connect(self.btn_2KM_on_cb)
        self.btn_2KM_off.setEnabled(False)
        self.btn_2KM_off.clicked.connect(self.btn_2KM_off_cb)
        self.btn_3KM_on.clicked.connect(self.btn_3KM_on_cb)
        self.btn_3KM_off.setEnabled(False)
        self.btn_3KM_off.clicked.connect(self.btn_3KM_off_cb)
        self.btn_5KM_on.clicked.connect(self.btn_5KM_on_cb)
        self.btn_5KM_off.setEnabled(False)
        self.btn_5KM_off.clicked.connect(self.btn_5KM_off_cb)
        self.btn_6KM_on.clicked.connect(self.btn_6KM_on_cb)
        self.btn_6KM_off.setEnabled(False)
        self.btn_6KM_off.clicked.connect(self.btn_6KM_off_cb)
        self.btn_7KM_on.clicked.connect(self.btn_7KM_on_cb)
        self.btn_7KM_off.setEnabled(False)
        self.btn_7KM_off.clicked.connect(self.btn_7KM_off_cb)
        self.btn_8KM_on.clicked.connect(self.btn_8KM_on_cb)
        self.btn_8KM_off.setEnabled(False)
        self.btn_8KM_off.clicked.connect(self.btn_8KM_off_cb)
        self.btn_9KM_on.clicked.connect(self.btn_9KM_on_cb)
        self.btn_9KM_off.setEnabled(False)
        self.btn_9KM_off.clicked.connect(self.btn_9KM_off_cb)
        self.btn_state_confirm.clicked.connect(self.pcs_state)
        self.btn_diesel_on.clicked.connect(self.diesel_on_cb)
        self.btn_diesel_off.clicked.connect(self.diesel_off_cb)

    def port_check(self):
        self.comboBox_port.clear()
        com = serial.Serial()
        coms_s = {}
        com_list = serial.tools.list_ports.comports()
        if len(com_list) <= 0:
            QMessageBox.critical(self, '错误', '无可用端口')
        else:
            for coms in com_list:
                coms_s['%s' % coms[0]] = '%s' % coms[1]
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
        port_info = [self.port, self.baud, self.parity, self.data, self.stop]
        self.port_connect = port_connection.port_connect(port_info)
        self.port_connect.oksignal.connect(self.checkok)
        self.port_connect.wrongsignal.connect(self.checkno)
        self.port_connect.start()
        self.port_connect.read_msg_signal.connect(self.val_update)
        self.btn_disconnect_port.setEnabled(True)
        self.groupBox_14.setEnabled(False)

    def checkno(self, str):
        QMessageBox.warning(self, 'Wrong', str)
        self.port_connect.port_state = 0

    def checkok(self, str):
        QMessageBox.warning(self, '提示', '%s串口已打开' % self.port)
        self.tabWidget.setEnabled(True)
        self.btn_checkport.setEnabled(False)
        self.btn_connect_port.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.port_signal.setPixmap(QPixmap('./image/green_pic.png'))
        self.manger_signal.setPixmap(QPixmap('./image/green_pic.png'))

    def port_close(self):
        self.port_connect.port_state = 0
        self.tabWidget.setEnabled(False)
        self.btn_checkport.setEnabled(True)
        self.btn_connect_port.setEnabled(True)
        self.groupBox_2.setEnabled(True)
        self.port_signal.setPixmap(QPixmap('./image/red_pic.png'))
        self.manger_signal.setPixmap(QPixmap('./image/red_pic.png'))
        self.btn_disconnect_port.setEnabled(False)

    def tcp_host(self):
        self.home_ip.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            self.home_ip.setText(str(my_addr))
        except:
            try:
                my_addr = socket.gethostbyname(socket.gethostbyname())
                self.home_ip.setText(str(my_addr))
            except:
                QMessageBox.warning(self, '错误', '无法获取IP，请连接网络！')
        finally:
            s.close()

    def tcp_connection(self):
        addr = self.aim_ip.text()
        port = int(self.aim_port.text())
        self.tcp_connect = tcp_connection.tcp_connnect(addr, port)
        self.tcp_connect.oksignal.connect(self.tcp_ok)
        self.tcp_connect.wrongsignal.connect(self.tcp_no)
        self.tcp_connect.start()
        self.tcp_connect.datasignal.connect(self.val_update)

    def tcp_ok(self, data):
        QMessageBox.information(self, 'OK', data)

    def tcp_no(self, data):
        QMessageBox.information(self, 'NO', data)

    def pcs_state(self):
        if self.pcs_on.isChecked():
            self.sig_pcs_flag = 1
        else:
            self.sig_pcs_flag = 0
            for i in range(0, 13):
                exec('self.%s.setText("%s")' % (self.pcs_val[i], ''))

    def btn_city_on_cb(self):
        msg = 'CITY IS ON'
        self.port_connect.send_msg(msg)
        self.ctiy_flag = 1
        self.btn_city_on.setEnabled(False)
        self.btn_city_off.setEnabled(True)

    def btn_city_off_cb(self):
        self.ctiy_flag = 0
        self.city_current_val.clear()
        self.city_voltage_val.clear()
        self.city_power_p_val.clear()
        self.city_power_q_val.clear()
        self.btn_city_off.setEnabled(False)
        self.btn_city_on.setEnabled(True)

    def btn_2KM_on_cb(self):
        msg = '2KM IS ON'
        self.port_connect.send_msg(msg)
        self.sig_2km_flag = 1
        self.btn_2KM_on.setEnabled(False)
        self.btn_2KM_off.setEnabled(True)

    def btn_2KM_off_cb(self):
        self.sig_2km_flag = 0
        self.btn_2KM_off.setEnabled(False)
        self.btn_2KM_on.setEnabled(True)

    def btn_3KM_on_cb(self):
        self.sig_pv_flag = 1
        msg = '3KM IS ON'
        self.port_connect.send_msg(msg)
        self.btn_3KM_on.setEnabled(False)
        self.btn_3KM_off.setEnabled(True)
        self.pv_signal.setPixmap(QPixmap('./image/green_pic.png'))

    def btn_3KM_off_cb(self):
        self.sig_pv_flag = 0
        self.pv_power_p_val.clear()
        self.pv_power_q_val.clear()
        self.pv_current_val.clear()
        self.btn_3KM_off.setEnabled(False)
        self.btn_3KM_on.setEnabled(True)
        self.pv_signal.setPixmap(QPixmap('./image/red_pic.png'))

    def btn_5KM_on_cb(self):
        self.sig_load1_flag = 1
        msg = '5KM IS ON'
        self.port_connect.send_msg(msg)
        self.btn_5KM_on.setEnabled(False)
        self.btn_5KM_off.setEnabled(True)

    def btn_5KM_off_cb(self):
        self.sig_load1_flag = 0
        self.load_1_q_val.clear()
        self.load_1_p_val.clear()
        self.load_1_current.clear()
        self.btn_5KM_off.setEnabled(False)
        self.btn_5KM_on.setEnabled(True)

    def btn_6KM_on_cb(self):
        self.sig_load2_flag = 1
        msg = '6KM IS ON'
        self.port_connect.send_msg(msg)
        self.btn_6KM_on.setEnabled(False)
        self.btn_6KM_off.setEnabled(True)

    def btn_6KM_off_cb(self):
        self.sig_load2_flag = 0
        self.load_2_q_val.clear()
        self.load_2_p_val.clear()
        self.load_2_current.clear()
        self.btn_6KM_off.setEnabled(False)
        self.btn_6KM_on.setEnabled(True)

    def btn_7KM_on_cb(self):
        self.sig_load3_flag = 1
        msg = '7KM IS ON'
        self.port_connect.send_msg(msg)
        self.btn_7KM_on.setEnabled(False)
        self.btn_7KM_off.setEnabled(True)

    def btn_7KM_off_cb(self):
        self.sig_load3_flag = 0
        self.load_3_q_val.clear()
        self.load_3_p_val.clear()
        self.load_3_current.clear()
        self.btn_7KM_off.setEnabled(False)
        self.btn_7KM_on.setEnabled(True)

    def btn_8KM_on_cb(self):
        self.groupBox_14.setEnabled(True)
        msg = '8QF IS ON'
        self.port_connect.send_msg(msg)
        self.btn_8KM_on.setEnabled(False)
        self.btn_8KM_off.setEnabled(True)
        self.diesel_signal.setPixmap(QPixmap('./image/green_pic.png'))

    def btn_8KM_off_cb(self):
        self.sig_diesel_flag = 0
        self.groupBox_14.setEnabled(False)
        self.btn_8KM_on.setEnabled(True)
        self.btn_8KM_off.setEnabled(False)
        self.diesel_signal.setPixmap(QPixmap('./image/red_pic.png'))

    def diesel_on_cb(self):
        self.sig_diesel_flag = 1

    def diesel_off_cb(self):
        self.sig_diesel_flag = 0
        for i in range(0, 16):
            exec('self.%s.setText("%s")' % (self.diesel_val[i], ''))

    def btn_9KM_on_cb(self):
        self.sig_bms_flag = 1
        msg = '9QF IS ON'
        self.port_connect.send_msg(msg)
        self.btn_9KM_on.setEnabled(False)
        self.btn_9KM_off.setEnabled(True)
        self.bms_signal.setPixmap(QPixmap('./image/green_pic.png'))

    def btn_9KM_off_cb(self):
        self.sig_bms_flag = 0
        self.btn_9KM_on.setEnabled(True)
        self.btn_9KM_off.setEnabled(False)
        self.bms_signal.setPixmap(QPixmap('./image/red_pic.png'))
        for i in range(0, 27):
            exec('self.%s.setText("%s")' % (self.bms_val[i], ''))

    def val_update(self, data):
        if data != ' ':
            val_get = data
            if self.ctiy_flag == 1:
                self.city_power_p_val.setText(str(int(val_get[0:4], 16)) + 'W')
                self.city_power_q_val.setText(str(int(val_get[4:8], 16)) + 'W')
                self.city_voltage_val.setText(
                    str(int(val_get[8:12], 16)) + 'V')
                self.city_current_val.setText(
                    str(int(val_get[12:16], 16)) + 'A')
            if self.sig_pv_flag == 1:
                self.pv_power_p_val.setText(str(int(val_get[16:20], 16)) + 'W')
                self.pv_power_q_val.setText(str(int(val_get[20:24], 16)) + 'W')
                self.pv_current_val.setText(str(int(val_get[24:28], 16)) + 'A')
            if self.sig_load1_flag == 1:
                self.load_1_p_val.setText(str(int(val_get[28:32], 16)) + 'W')
                self.load_1_q_val.setText(str(int(val_get[32:36], 16)) + 'W')
                self.load_1_current.setText(str(int(val_get[36:40], 16)) + 'A')
            if self.sig_load2_flag == 1:
                self.load_2_p_val.setText(str(int(val_get[40:44], 16)) + 'W')
                self.load_2_q_val.setText(str(int(val_get[44:48], 16)) + 'W')
                self.load_2_current.setText(str(int(val_get[48:52], 16)) + 'A')
            if self.sig_load3_flag == 1:
                self.load_3_p_val.setText(str(int(val_get[52:56], 16)) + 'W')
                self.load_3_q_val.setText(str(int(val_get[56:60], 16)) + 'W')
                self.load_3_current.setText(str(int(val_get[60:64], 16)) + 'A')
            if self.sig_bms_flag == 1:
                for i in range(0, 27):
                    exec('self.%s.setText("%s")' %
                         (self.bms_val[i],
                          str(int(val_get[64 + 4 * i:68 + 4 * i], 16))))
            if self.sig_pcs_flag == 1:
                for i in range(0, 13):
                    exec('self.%s.setText("%s")' %
                         (self.pcs_val[i],
                          str(int(val_get[162 + 4 * i:166 + 4 * i], 16))))
            if self.sig_diesel_flag == 1:
                for i in range(0, 16):
                    exec('self.%s.setText("%s")' %
                         (self.diesel_val[i],
                          str(int(val_get[204 + 4 * i:208 + 4 * i], 16))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = JY_Main()
    win.show()
    sys.exit(app.exec_())
