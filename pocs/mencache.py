import socket


def poc(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("stats\r\n".encode())
        recv_data = s.recv(1024)
        s.close()
        if recv_data and b"STAT pid" in recv_data:
            return "memcached is unauthorized"
    except:
        pass
    return None
