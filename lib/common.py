from colorama import init, Fore, Style
from urllib.parse import urlparse
import socket

init(autoreset=True)


class ColorPrint:
    @staticmethod
    def white(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.WHITE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def green(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.GREEN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def cyan(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.CYAN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def red(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.RED + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def blue(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.BLUE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def yellow(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.YELLOW + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)


def getip(url):
    """
    url: http://www.baidu.com:80/index.php?id=1&uid=2
    return ['14.215.177.39', '14.215.177.38']
    """
    if not url.startswith("http"):
        url = "http://" + url
    o = urlparse(url)
    domain = o.hostname
    ip = socket.gethostbyname_ex(domain)
    return ip[2]

color_print = ColorPrint()