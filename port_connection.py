import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import time


class port_connect(QThread):
    oksignal = pyqtSignal(str)
    wrongsignal = pyqtSignal(str)
    closesignal = pyqtSignal(str)
    read_msg_signal = pyqtSignal(str)

    def __init__(self, list):
        super().__init__()
        self.port_state = 0
        self.port_info = list

    def run(self):
        self.ser = serial.Serial()
        self.ser.port = self.port_info[0]
        self.ser.baudrate = self.port_info[1]
        self.ser.parity = self.port_info[2]
        self.ser.bytesize = self.port_info[3]
        self.ser.stopbit = self.port_info[4]
        self.serCloseFlag = 0
        try:
            self.ser.open()
            self.port_state = 1
            self.oksignal.emit('OK')

        except:
            self.wrongsignal.emit('当前端口无法打开')
            self.port_state = 0

        while self.port_state == 1:
            self.read()
            time.sleep(1)

    def read(self):
        try:
            num = self.ser.inWaiting()
            print(num)

        except:
            self.ser.close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            out_s = ''
            for i in range(0, num):
                out_s = out_s + '{:02X}'.format(data[i])
            if out_s[0:4] == 'ABFF' and out_s[-4:] == 'ABFF':
                self.read_msg_signal.emit(out_s)
        else:
            pass

    def send_msg(self, msg):
        if self.ser.isOpen():
            msg_s = msg.strip()
            msg_s = bytes(msg_s.encode('utf-8'))
            self.ser.write(msg_s)
            print(msg)
        else:
            pass
