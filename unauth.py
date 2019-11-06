from lib.common import getip, color_print
from lib.poc import *
import time
import threading
import queue
import sys
from lib.cmdline import cmdLineParser

thread_count_lock = threading.Lock()


def generate_tasks(hosts, ports):
    task_queue = queue.Queue()
    poc_list = ['redis', 'mongo', 'genkins', 'memcached', 'jboss', 'zookeeper',
                'rsync', 'couchdb', 'elasticsearch', 'hadoop', 'jupyter',
                'docker', 'ftp', 'smb', 'postgresql', 'oracle', "mssql", 'mysql']
    # poc_list = ['mysql']
    for poc in poc_list:
        for host in hosts:
            if len(ports) > 0:
                [task_queue.put({"host": host, "poc": poc, "port": port}) for port in ports]
            else:
                task_queue.put({"host": host, "poc": poc, "port": None})
    return task_queue


def scan(task_queue):
    global thread_count
    while task_queue.qsize() > 0:
        task = task_queue.get()
        if task['port']:
            globals()[task['poc']](task['host'], task['port'])
        else:
            globals()[task['poc']](task['host'])
    thread_count_lock.acquire()
    thread_count = thread_count - 1
    thread_count_lock.release()


def run(task_queue):
    for i in range(thread_count):
        t = threading.Thread(target=scan, args=(task_queue, ))
        t.setDaemon(True)
        t.start()
    while thread_count > 0:
        time.sleep(1)


def load_host(args):
    host_list = []
    if args.host:
        host_list.append(getip(args.host.strip()))
        color_print.cyan(f"[*] load host to scan: {host_list[0]}")
    elif args.host_file:
        try:
            with open(args.host_file, 'r', encoding='utf-8') as f:
                for target in f.readlines():
                    host_list.append(getip(target.strip()))
            color_print.cyan(f"[*] load host file to scan: {args.host_file}")
        except Exception as e:
            color_print.red(f"[-] error host_file: {args.host_file}\n[-] {e}")
            sys.exit()
    # exclude empty elements and remove duplicates
    host_list = list(set(filter(None, host_list)))

    if len(host_list) < 1:
        color_print.red(f"[-] no target to scan, use -H/-HF to specify target")
        sys.exit()
    return host_list


if __name__ == "__main__":
    start_time = time.time()
    global thread_count
    args = cmdLineParser()
    # get host
    hosts = load_host(args)

    # get port list
    ports = []
    if args.port:
        ports = [int(port) for port in args.port.split(',')]
        color_print.cyan(f"[*] begin to scan ports: {ports}")
    else:
        color_print.cyan(f"[*] begin to scan default ports")

    # generate tasks
    task_queue = generate_tasks(hosts, ports)
    color_print.cyan(f"[*] task count：{task_queue.qsize()}")

    # get thread count
    thread_count = args.thread if args.thread and args.thread < 200 else 100
    if thread_count >= task_queue.qsize():
        thread_count = task_queue.qsize()
    color_print.cyan(f"[*] set thread count: {thread_count}")

    # run
    run(task_queue)
    color_print.white(f"done with time: {time.time()-start_time}s")