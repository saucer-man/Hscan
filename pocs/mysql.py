import traceback

import pymysql


def poc(host, port, timeout):
    try:
        conn = pymysql.connect(host=host, port=port, user="root", password="123456",
                               db='mysql', connect_timeout=timeout, read_timeout=timeout, write_timeout=timeout)
        conn.close()
        return "mysql weak password:root/123456"
    except:
        # traceback.print_exc()
        if "Access denied for user" in traceback.format_exc():
            return "detected mysql service"
    return None
