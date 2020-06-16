import subprocess
import os
import subprocess

from libs.core.data import logger, conf
from libs.core.exception import TargetException2


def ping(ip):
    if os.name == "nt":
        return winping(ip)
    else:
        return unixping(ip)


# 判断主机是否存活
def unixping(ip):
    try:
        p = subprocess.Popen([f"ping -c 1 -W 20 {ip}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        out = p.stdout.read()
        if "ttl" in str(out):
            return True
        else:
            return False
    except:
        return False


def winping(ip):
    try:
        p = subprocess.Popen(['ping', '-n', '1', '-w', '20', ip],
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        output = p.stdout.read().decode("gbk").upper()
        if "TTL" in output:
            return True
        else:
            return False
    except:
        return False


def alive_detect():
    tmp = set()  # 暂时用来存放一下存活的主机
    if conf.alive_detect:
        logger.info("host alive detection...")
        for target in conf.target:
            if ping(target):
                logger.debug(f"{target} is alive")
                tmp.add(target)
            else:
                logger.debug(f"{target} is dead")
        conf.target = tmp
    else:
        logger.info("skip host alive detection because you use -Pn")
    if len(conf.target) < 1:
        raise TargetException2
    with open(conf.output_path, "a", encoding='utf-8') as f:
        f.write("1. alive host\n")
        for t in conf.target:
            f.write(t + '\n')
        f.write('\n\n')
