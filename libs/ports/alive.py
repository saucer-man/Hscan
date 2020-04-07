import os
import subprocess
import os
from libs.core.data import cmdLineOptions, logger, conf
from libs.core.exception import PyVersionException, TargetException1, TargetException2
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1


def ping(ip):
    if os.name == "nt":
        return winping(ip)
    else:
        return unixping(ip)

# 判断主机是否存活
def unixping(ip):
    try:
        p = subprocess.Popen([f"ping -c 1 -W 20 {ip}"], stdin=subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
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
    tmp = set()   # 暂时用来存放一下存活的主机
    if cmdLineOptions.alive_detect:
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
