import socket


def poc(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("envi".encode())
        recv_data = s.recv(1024)
        s.close()
        if b'zookeeper.version' in recv_data:
            return "zookeeper is unauthorized"
    except:
        pass
    return None