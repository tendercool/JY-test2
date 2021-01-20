from PyQt5.Qt import QThread,QObject
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo


class port_connect(QObject):
    def __init__(self):
        super().__init__()
        self.port_state = 0
        self.ser = QSerialPort()
        self.ser_info = QSerialPortInfo()
        


    def run(self):
        if self.check_signal != '':
            self.check()
        self.connect()
        self.disconnect()
        self.send()
        self.read()

    def check(self):
        self.com_dic = {}
        port_info = QSerialPortInfo()
        for port in port_info:
            self.com_dict['%s' % port[0]] = '%s' % port[1]
            print(self.com_dict)
        self.port_list.emit(str(self.com_dic))

    def connect(self):
        pass

    def disconnect(self):
        pass

    def read(self):
        pass

    def send(self):
        pass
