
from pickle import dumps, loads
import socket

CSPROTO = dict({
    "EMPTY": b"",
    "END": b"<F2B_END_COMMAND>",
    "CLOSE": b"<F2B_CLOSE_COMMAND>"
})


def convert(m):
    """Convert every "unexpected" member of message to string"""
    if isinstance(m, (str, bool, int, float, list, dict, set)):
        return m
    else:  # pragma: no cover
        return str(m)


def receive(sock):
    msg = CSPROTO['EMPTY']
    bufsize = 1024
    while msg.rfind(CSPROTO['END'], -32) == -1:
        chunk = sock.recv(bufsize)
        if not len(chunk):
            raise socket.error(104, 'Connection reset by peer')
        if chunk == CSPROTO['END']:
            break
        msg = msg + chunk
        if bufsize < 32768:
            bufsize <<= 1
    return loads(msg)


class CSocket:

    def __init__(self, sock="/var/run/fail2ban/fail2ban.sock", timeout=-1):
        self.__csock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__deftout = self.__csock.gettimeout()
        if timeout != -1:
            self.settimeout(timeout)
        self.__csock.connect(sock)

    def __del__(self):
        self.close()

    def send(self, msg):
        # Convert every list member to string

        obj = dumps(msg)
        self.__csock.send(obj)
        self.__csock.send(CSPROTO['END'])
        return receive(self.__csock)

    def settimeout(self, timeout):
        self.__csock.settimeout(timeout if timeout != -1 else self.__deftout)

    def close(self):
        if not self.__csock:
            return
        try:
            self.__csock.sendall(CSPROTO['CLOSE'] + CSPROTO['END'])
            self.__csock.shutdown(socket.SHUT_RDWR)
        except socket.error:  # pragma: no cover - normally unreachable
            pass
        try:
            self.__csock.close()
        except socket.error:  # pragma: no cover - normally unreachable
            pass
        self.__csock = None
