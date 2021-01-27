from PyQt5.Qt import QObject
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox,QWidget
from PyQt5.QtCore import QThread,pyqtSignal


class port_connect(QObject):
    oksignal = pyqtSignal(str)
    wrongsignal = pyqtSignal(str)
    closesignal = pyqtSignal(str)
    read_msg_signal = pyqtSignal(str)
    def __init__(self,list):
        super().__init__()
        self.port_state = 0
        # self.ser = serial.Serial()
        # self.ser.port = port
        # self.ser.baudrate = baud
        # self.ser.parity = parity
        # self.ser.bytesize = data
        # self.ser.stopbit = stop
        self.port_info = list
        # self.ser.port = self.port_info[0]
        # self.ser.baudrate = self.port_info[1]
        # self.ser.parity = self.port_info[2]
        # self.ser.bytesize = self.port_info[3]
        # self.ser.stopbit = self.port_info[4]
        # self.connect()
        
       

    def connect(self):
        self.ser = serial.Serial()
        self.ser.port = self.port_info[0]
        self.ser.baudrate = self.port_info[1]
        self.ser.parity = self.port_info[2]
        self.ser.bytesize = self.port_info[3]
        self.ser.stopbit = self.port_info[4]
        try:
            self.ser.open()
            # print(self.ser.port)
            self.oksignal.emit('OK')
               
        except:
            # QMessageBox.critical(self,'错误','当前端口无法打开')
            self.wrongsignal.emit('当前端口无法打开')

    # def disconnect(self):
    #     self.ser.close()  
        self.read()
        

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
            self.read_msg_signal.emit(out_s)
            
    def send_msg(self,msg):
        if self.ser.isOpen():
            msg_s = msg.strip()
            msg_s = bytes(msg_s.encode('utf-8'))
            self.ser.write(msg_s)

