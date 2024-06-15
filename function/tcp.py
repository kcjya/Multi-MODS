from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TCP_Server(QThread):
    connected = pyqtSignal(tuple)
    recieved = pyqtSignal(tuple)

    def __init__(self, _ip, _port, _max):
        super().__init__()
        self.ip = _ip
        self.port = _port
        self.max = _max

    def run(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen(self.max)
            while True:
                client_socket, addr = server_socket.accept()
                self.connected.emit((client_socket, addr[0], addr[1]))
                client_socket.sendall("'fire.png'检测完成！结果如下:1项fire;".encode("utf-8"))
                client_thread = TCP_Cilent(_socket=client_socket, _signal=self.recieved, _ip=addr[0])
                client_thread.start()
                # print(type(client_socket))
        except:
            pass


class TCP_Cilent(QThread):
    def __init__(self, _socket, _signal, _ip):
        super().__init__()
        self.client_socket = _socket
        self._signal = _signal
        self._ip = _ip

    def run(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self._signal.emit((self._ip, data.decode()))
            except:
                pass

        self.client_socket.close()

