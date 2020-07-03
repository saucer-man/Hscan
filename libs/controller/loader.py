import importlib
import logging
import os
import queue
import sys
import time
import traceback

from libs.core.common import url2ip
from libs.core.data import cmdLineOptions, logger, paths, conf
from libs.core.exception import TargetException1, PocTaskException
from libs.utils.config import ConfigFileParser


def loader():
    general()
    poc_loader()
    target_loader()
    port_loader()
    engine_loader()


def general():
    if cmdLineOptions.verbose or ConfigFileParser().verbose().strip() == "True":
        logger.logger.setLevel(logging.DEBUG)
    filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt'
    conf.output_path = os.path.join(paths.RESULT_PATH, filename)


def engine_loader():
    conf.timeout = cmdLineOptions.timeout

    # load alive_detect
    if cmdLineOptions.alive_detect and ConfigFileParser().alive_detect().strip() == "True":
        conf.alive_detect = True
    else:
        conf.alive_detect = False

    # load port_scan
    if cmdLineOptions.port_scan and ConfigFileParser().port_scan().strip() == "True":
        conf.port_scan = True
    else:
        conf.port_scan = False

    if conf.port_scan:
        # Load port scan concurrency
        try:
            if isinstance(cmdLineOptions.port_scan_threads, int):
                conf.port_scan_thread = cmdLineOptions.port_scan_threads

            elif isinstance(ConfigFileParser().port_scan_thread(), int):
                conf.port_scan_thread = ConfigFileParser().port_scan_thread()
            else:
                conf.port_scan_thread = 200
        except:
            conf.port_scan_thread = 200

    # Load pocs scan concurrency
    try:
        if isinstance(cmdLineOptions.thread, int):
            conf.thread = cmdLineOptions.thread
        else:
            conf.thread = int(ConfigFileParser().thread())
    except:
        conf.thread = 100


def port_loader():
    conf.port = set()
    # first load port from args
    if cmdLineOptions.port:
        ports = cmdLineOptions.port.split(",")
        for port in ports:
            if "-" in port:
                for i in range(int(port.split("-")[0]), int(port.split("-")[-1]) + 1):
                    conf.port.add(i)
            else:
                conf.port.add(int(port))
    # otherwise load port from config file
    elif ConfigFileParser().port():
        ports = ConfigFileParser().port().split(",")
        for port in ports:
            if "-" in port:
                for i in range(int(port.split("-")[0]), int(port.split("-")[-1]) + 1):
                    conf.port.add(i)
            else:
                conf.port.add(int(port))
    # otherwise scan all ports
    else:
        conf.port = set([i for i in range(1, 65536)])


def target_loader():
    conf.target = set()
    # Load the target specified in the command line or the file, because it is a host scanner, the target is replaced by the host form
    if cmdLineOptions.url:
        conf.target.add(url2ip(cmdLineOptions.url))
        logger.info(f"loader target: {cmdLineOptions.url}-->{url2ip(cmdLineOptions.url)}")
    if cmdLineOptions.target_file:
        with open(cmdLineOptions.target_file, "r", encoding='utf-8') as f:
            for line in f.readlines():
                conf.target.add(url2ip(line.strip()))
        logger.info(f"loader target from : {cmdLineOptions.target_file}")
    # Load the targets in the conf configuration file
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

    if conf.poctask_queue.qsize() < conf.thread:
        conf.thread = conf.poctask_queue.qsize()

    if conf.poctask_queue.qsize() < 1:
        raise PocTaskException
    conf.poctask_num = conf.poctask_queue.qsize()
    logger.info(f"total tasks: {conf.poctask_queue.qsize()}")
