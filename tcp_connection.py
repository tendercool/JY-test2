import sys
from PyQt5.QtWidgets import QWidget
import socket

class tcp_connnect(QWidget):
    def __init__(self):
        super().__init__()
        self.my_socket = socket.socket()

    def tcp_confirm(self,addr,port):
        host = addr
        ports = port
        self.my_socket.connect(host,port)

