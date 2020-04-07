import socket
import binascii
import traceback


def poc(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex(
        "430000000300000000000000d40700000000000061646d696e2e24636d640000000000ffffffff1c000000016c69737444617461626173657300000000000000f03f00")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.send(payload)
        recv_data = s.recv(1024)
        if b"databases"in recv_data:
            return f"mongodb is unauthorized"
        if b"Unauthorized" in recv_data:
            return f"mongodb service(authorized)"
    except:
        # traceback.print_exc()
        pass
    finally:
        s.close()