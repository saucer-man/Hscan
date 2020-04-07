import binascii
import socket


def poc(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex("1001010400000000fc00000001000071001000000683f2f8602e000000000000e001000088ffffff3604000056000d00700002007400090086000d00a000140000000000c8000a00dc000a00f0000600000000000000fc000000fc00000059005400530048004c005400310039003000360030003200370073006100b0a5d2a5f3a5b6a586a596a5e6a5f6a5c6a5700079006d007300730071006c003d0032002e0031002e0034003100390032002e003100360038002e003100330036002e003100320038003a003100340033003300440042002d004c00690062007200610072007900750073005f0065006e0067006c006900730068006d0061007300740065007200")
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(payload)
        recv_data = s.recv(1024)
        s.close()
        # print(binascii.b2a_hex(recv_data))
        # master
        if b"6d00610073007400650072" in binascii.b2a_hex(recv_data):
            return "mssql weak password：sa\Qwe123456"
        # Login failed
        elif b"27007300610027" in binascii.b2a_hex(recv_data):
            return "detected mssql service"
    except:
        # traceback.print_exc()
        pass
    return None