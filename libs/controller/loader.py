from libs.core.common import url2ip
from libs.core.data import cmdLineOptions, logger, paths, conf
from libs.utils.config import ConfigFileParser
import os
import sys
from libs.core.exception import PyVersionException, TargetException1, PocTaskException
import queue
import importlib
import traceback
def loader():
    poc_loader()
    target_loader()
    port_loader()
    engine_loader()

def engine_loader():
    conf.timeout = cmdLineOptions.timeout

def port_loader():
    conf.port = set()
    if ConfigFileParser().port():
        ports = ConfigFileParser().port().split(",")
        for port in ports:
            conf.port.add(port.strip())
    else:
        conf.port = set([i for i in range(1, 65546)])



def target_loader():
    conf.target = set()
    # 加载命令行指定的或者file里面的target，因为是主机扫描器，所以target统一被换成host形式
    if cmdLineOptions.url:
        conf.target.add(url2ip(cmdLineOptions.url))
        logger.info(f"loader target: {cmdLineOptions.url}-->{url2ip(cmdLineOptions.url)}")
    if cmdLineOptions.target_file:
        with open(cmdLineOptions.target_file, "r", encoding='utf-8') as f:
            for line in f.readlines():
                conf.target.add(url2ip(line.strip()))
        logger.info(f"loader target from : {cmdLineOptions.target_file}")
    # 加载conf配置文件里的命令行
    if not paths.CONFIG_PATH:
        return
    if ConfigFileParser().target_url():
        url = ConfigFileParser().target_url
        conf.target.add(url2ip(url))
        logger.info(f"loader target: {url}-->{url2ip(url)}")

    if ConfigFileParser().target_url():
        target_file = ConfigFileParser().target_url()
        with open(target_file, "r", encoding='utf-8') as f:
            for line in f.readlines():
                conf.target.add(url2ip(line.strip()))
        logger.info(f"loader target from : {target_file}")
    if len(conf.target) < 1:
        raise TargetException1

    logger.info(f"total number of scan host targets : {len(conf.target)}")


def poc_loader():
    conf.pocs = set()
    if ConfigFileParser().poc_list():
        logger.info(f"loader pocs from config file...")
        for poc in ConfigFileParser().poc_list().split(","):
            conf.pocs.add(poc.strip())
    else:
        logger.info(f"loader all pocs...")
        poc_name_list = os.listdir(paths.POCS_PATH)
        for poc in poc_name_list:
            if poc not in ['__init__.py', 'test.py'] and poc.endswith('.py'):
                conf.pocs.add(os.path.splitext(poc)[0])

    logger.info(f"loaded pocs : {conf.pocs}")
    logger.info(f"total number of poc script : {len(conf.pocs)}")


def load_poctasks():
    logger.info(f"generate poc tasks...")
    sys.path.insert(0, paths.POCS_PATH)
    conf.poctask_queue = queue.Queue()
    for poc in conf.pocs:
        try:
            p = importlib.import_module(f'{poc}')
            for host, port_list in conf.target_port_dict.items():
                for port in port_list:
                    conf.poctask_queue.put({"host": host, "poc": p, "port": port})
        except:
            traceback.print_exc()


    if conf.poctask_queue.qsize() < 1:
        raise PocTaskException
    logger.info(f"total tasks: {conf.poctask_queue.qsize()}")
