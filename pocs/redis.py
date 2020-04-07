import socket
import traceback


def poc(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    try:
        s.connect((host, port))
        s.send(payload.encode('utf-8'))
        recv_data = s.recv(1024)
        if recv_data and b'redis_version' in recv_data:
            return f'redis is unauthorized to access'
        elif b'NOAUTH Authentication required' in recv_data:
            return f"redis service(authorized)"
        elif b"protected mode is enabled" in recv_data:
            return f"redis service(protected mode)"
    except:
        # traceback.print_exc()
        pass
    finally:
        s.close()
