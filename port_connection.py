from PyQt5.Qt import QThread,QObject
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox,QWidget


class port_connect(QWidget):
    def __init__(self):
        super().__init__()
        self.port_state = 0
        self.ser = serial.Serial()
  

    def connect(self,port,baud,parity,data,stop):
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.parity = parity
        self.ser.bytesize = data
        self.ser.stopbit = stop
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self,'错误','当前端口无法打开')

    def disconnect(self):
        self.ser.close()

    def read(self):
        try:
            num = self.ser.isWating()
        except :
            self.ser.close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            out_s = ''
            for i in range(0,num):
                out_s = out_s + '{:02X}'.format(data[i])
            return out_s
            
    def send_msg(self,msg):
        if self.ser.isOpen():
            msg_s = msg
            msg_s = msg_s.strip()
            msg_s = bytes(msg_s.encode('utf-8'))
            self.ser.write(msg_s)

