from PyQt5.Qt import QThread,QObject
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo


class port_connect(QObject):
    def __init__(self):
        super().__init__()
        self.port_state = 0
        self.ser = QSerialPort()
        self.ser_info = QSerialPortInfo()

        self.check()


    def set_port(self):
        if self.check_signal != '':
            self.check()
        self.connect()
        self.disconnect()
        self.send()
        self.read()

    def check(self):
        port_info = self.ser_info.availablePorts()
        for port in port_info:
            port_id = port.portName()
        return port_id

    def connect(self):
        pass

    def disconnect(self):
        pass

    def read(self):
        pass

    def send(self):
        pass
