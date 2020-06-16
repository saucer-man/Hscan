from ftplib import FTP


def poc(host, port, timeout):
    try:
        ftp = FTP(timeout=timeout)
        ftp.connect(host, port)
        try:
            ftp.login('anonymous', 'guest@guest.com')
            return "ftp is unauthorized"
        except:
            return "ftp service detected"
        ftp.quit()
    except:
        pass
    return None
