import socket
import binascii


def poc(host, port, timeout):
    # try:
    #     conn = psycopg2.connect(host=host, port=port, database="postgres",
    #                             user="postgres", password="123456", connect_timeout=timeout)
    #     conn.close()
    #     color_print.red(f"[+] postgresql is not authorized：{host}:{port}:postgres：123456")
    # except:
    #     if "no pg_hba.conf entry" in traceback.format_exc():
    #         color_print.green(f"[+] postgresql service detected (local login only)：{host}:{port}")

    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex("00000029000300007573657200706f73746772657300646174616261736500706f7374677265730000")
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(payload)
        recv_data = s.recv(1024)
        s.close()
        # print(binascii.b2a_hex(recv_data))
        # no pg_hba.conf
        if b"70675f6862612e636f6e66" in binascii.b2a_hex(recv_data):
            return "postgresql service detected (local login only)"
        # R
        elif binascii.b2a_hex(recv_data).startswith(b"520000000c0000000"):
            return "postgresql service detected (need password)"
        # server_version
        elif b"7365727665725f76657273696f6e" in binascii.b2a_hex(recv_data):
            return "postgresql is unauthorized"
    except:
        # traceback.print_exc()
        pass
    return None