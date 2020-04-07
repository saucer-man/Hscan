import socket
from libs.core.data import conf, logger
import gevent
import queue
import sys

def scan():
    while not conf.port_scan_task.empty():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(conf.timeout)
        port_task = conf.port_scan_task.get()
        host = port_task["host"]
        port = port_task["port"]
        logger.debug(f"port scan {host}:{port} ...")
        sys.stdout.write("(" + str(conf.port_scan_task_num - conf.port_scan_task.qsize()) + "/" + str(conf.port_scan_task_num) + ")\r")
        sys.stdout.flush()
        try:
            s.connect((host, int(port)))
            conf.target_port_dict[host].append(int(port))
            logger.debug(f"port open {host}:{port}")
        except Exception as e:
            pass
        finally:
            s.close()



def generate_portscan_task():
    conf.port_scan_task = queue.Queue()
    for host in conf.target:
        for port in conf.port:
            conf.port_scan_task.put({"host": host, "port": port})


def portscan():
    conf.target_port_dict = {}   # 这是个字典，键为host，值为host中开放的端口列表
    for host in conf.target:
        conf.target_port_dict[host] = []

    if conf.port_scan:
        generate_portscan_task()
        conf.port_scan_task_num = conf.port_scan_task.qsize()
        if conf.port_scan_thread > conf.port_scan_task_num:
            conf.port_scan_thread = conf.port_scan_task_num
        logger.info(f"start to port scan...  (threads:{conf.port_scan_thread})")
        gevent.joinall([gevent.spawn(scan) for _ in range(0, conf.port_scan_thread)])
        for host, port in conf.target_port_dict.items():
            logger.info(f"detect {host} opened {len(port)} ports: {port}")
    else:
        logger.info("skip open port scan")
        for host, port in conf.target_port_dict.items():
            conf.target_port_dict[host] = [int(i) for i in conf.port]

    with open(conf.output_path, "a", encoding='utf-8') as f:
        f.write("2. open port\n")
        for host, port in conf.target_port_dict.items():
            f.write(host + ': ' + str(port)+'\n')
        f.write('\n\n')

