import sys
from PyQt5.QtCore import QThread,pyqtSignal
import socket,time

class tcp_connnect(QThread):
    oksignal = pyqtSignal(str)
    wrongsignal = pyqtSignal(str)
    datasignal = pyqtSignal(str)
    def __init__(self,addr,port):
        super().__init__()
        self.my_socket = socket.socket()
        self.tcp_state = 0
        self.host = addr
        self.ports = port


    def run(self):
        try:
            self.my_socket.connect(self.host,self.port)
            self.tcp_state = 1
            self.oksignal.emit('OK')
        except :
            self.tcp_state = 0
            self.wrongsignal.emit('连接失败！')
        while self.tcp_state == 1:
            self.tcp_confirm()
            time.sleep(1)

    def tcp_confirm(self):
        receive_data = self.tcp_socket.accept(1024)
        receive_data.decode(encoding = 'utf-8')
        self.datasignal.emit(receive_data)

    def tcp_send(self,data):
        send_data = data.encode(encoding='utf-8')
        self.tcp_socket.send(send_data)