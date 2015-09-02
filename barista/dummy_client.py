import sys
import socket
import barista


class DummyClient:
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))

    def send(self, msg):
        msg_length = len(msg)
        totalsent = 0
        while totalsent < msg_length:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def recv(self, bufsize=1024):
        response = ""
        while True:
            chunk = self.sock.recv(1024)
            if not chunk:
                break
            response += chunk
        return response

    def __del__(self):
        self.sock.close()

if __name__ == "__main__":
    N = 1
    if len(sys.argv) == 2:
        N = int(sys.argv[1])

    for i in xrange(N):
        client = DummyClient('127.0.0.1', 50001)
        #client = DummyClient('127.0.0.1', 6379)
        client.send(barista.GRAD_UPDATE)
        response = client.recv()
        print "Response[%d]:" % i, response
