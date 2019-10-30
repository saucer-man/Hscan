from colorama import init, Fore, Style
from urllib.parse import urlparse
import socket
import threading

init(autoreset=True)
lock = threading.Lock()


class ColorPrint:
    @staticmethod
    def white(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.WHITE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

    @staticmethod
    def green(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.GREEN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

    @staticmethod
    def cyan(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.CYAN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

    @staticmethod
    def red(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.RED + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

    @staticmethod
    def blue(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.BLUE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

    @staticmethod
    def yellow(s, end='\n', flush=False):
        lock.acquire()
        print(Style.BRIGHT+Fore.YELLOW + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)
        lock.release()

def getip(url):
    """
    url: http://www.baidu.com:80/index.php?id=1&uid=2
    return ['14.215.177.39', '14.215.177.38']
    """
    url = url.strip()
    if not url.startswith("http"):
        url = "http://" + url
    try:
        o = urlparse(url)
        domain = o.hostname
        ip = socket.gethostbyname(domain)
    except:
        return None
    return ip



color_print = ColorPrint()