import os
import socket
from urllib.parse import urlparse

from libs.core.data import logger
from libs.core.data import paths


def banner():
    return """
     < welcome to hscan. >
  -----------------------
         \   ^__^
          \  (oo)\_______
             (__)\       )\\
                 ||----w |
                 ||     ||
                 """


# set paths of project
def set_paths(module_path):
    paths.ROOT_PATH = module_path
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH, "config.conf")
    paths.POCS_PATH = os.path.join(paths.ROOT_PATH, "pocs")
    paths.RESULT_PATH = os.path.join(paths.ROOT_PATH, "result")

    if not os.path.isfile(paths.CONFIG_PATH):
        err_msg = 'Config files missing, it may cause some issues.\n'
        logger.error(err_msg)
    if not os.path.exists(paths.POCS_PATH):
        logger.error("pocs file missing")
        os.mkdir(paths.POCS_PATH)

    if not os.path.exists(paths.RESULT_PATH):
        os.mkdir(paths.RESULT_PATH)


def url2ip(url):
    """
    url: http://www.baidu.com:80/index.php?id=1&uid=2
    return '14.215.177.39'
    """
    if not url.startswith("http"):
        url = "http://" + url
    o = urlparse(url)
    domain = o.hostname
    host = socket.gethostbyname(domain)
    return host
