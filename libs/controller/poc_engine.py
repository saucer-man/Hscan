#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from libs.core.data import logger, conf
import gevent
import sys

def poc_scan():
    while conf.poctask_queue.qsize() > 0:
        task = conf.poctask_queue.get()
        res = task["poc"].poc(task['host'], task['port'], conf.timeout)
        result_handler(task, res)
        sys.stdout.write("(" + str(conf.poctask_num -conf.poctask_queue.qsize()) + "/" + str(conf.poctask_num) + ")\r")
        sys.stdout.flush()


def result_handler(task, res):
    if not res:
        return
    logger.warning(f"{task['host']}:{task['port']} --> {res}")
    with open(conf.output_path, "a", encoding='utf-8') as f:
        f.write(f"{task['host']}:{task['port']} --> {res}\n")

def run():
    logger.info(f"begin poc scan...  (threads: {conf.thread})")
    with open(conf.output_path, "a", encoding='utf-8') as f:
        f.write("3. pocs scan\n")
    gevent.joinall([gevent.spawn(poc_scan) for _ in range(0, conf.thread)])
    logger.info(f"the scan is over and the results are saved in {conf.output_path}")