from PyQt5.Qt import QThread,QObject
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox,QWidget


class port_connect(QWidget):
    def __init__(self):
        super().__init__()
        self.port_state = 0
        self.ser = serial.Serial()

    def set_port(self):
        
        self.connect()
        self.disconnect()
        self.send()
        self.read()

    

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
        pass

    def send(self):
        pass
