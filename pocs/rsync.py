import socket

# rsync unauthorized

def poc(host, port, timeout):
    # refer: https://github.com/JE2Se/VayneScan/blob/master/poc/rsyncunauth.py
    try:
        payload = b"\x40\x52\x53\x59\x4e\x43\x44\x3a\x20\x33\x31\x2e\x30\x0a"
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(payload)
        initinfo = s.recv(400)
        if b"RSYNCD" in initinfo:
            s.sendall(b"\x0a")
            path = s.recv(200)
            s.close()
            if len(path) > 0:
                return "rsync is unauthorized"
            return "detect rsync service"
    except Exception as e:
        pass
        # print(e)
    return None