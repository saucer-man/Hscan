import socket
import re

def poc(host, port, timeout):
    # refer: https://raw.githubusercontent.com/ysrc/xunfeng/master/vulscan/vuldb/rsync_weak_auth.py
    def _rsync_init(host, port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        s.connect((host, port))
        s.send("@RSYNCD: 31\n".encode())
        _ = s.recv(1024)
        return s

    try:
        # get directory
        s = _rsync_init(host, port)
        s.send(bytes.fromhex('0a'))
        recv_data = s.recv(1024)
        s.close()
        paths = []
        if recv_data:
            for path_name in re.split('\n', recv_data.decode()):
                if path_name and not path_name.startswith('@RSYNCD: '):
                    paths.append(path_name.split('\t')[0].strip())
        if paths:
            # print(f"get directory bytes-----{recv_data}")
            # print(f"The obtained directory is-----------{paths}")

            # Try to see if can gain unauthorized access
            for path in paths:
                s = _rsync_init(host, port)
                s.send(f"{path}\n".encode())
                recv_data = s.recv(1024)
                # print(f" Trying to grant unauthorized access to the accepted bytes-----------{recv_data}")

                if recv_data.decode() == '\n':
                    recv_data = s.recv(1024)
                # The following instructions prove unauthorized access
                if recv_data.decode().startswith('@RSYNCD: OK'):
                    return "[+] rsync is unauthorized"
                s.close()
            return "detected rsync service"
    except:
        # traceback.print_exc()
        pass
    return None