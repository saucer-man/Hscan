#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from libs.core.data import logger, conf
import sys

def poc_scan():
    while conf.poctask_queue.qsize() > 0:
        task = conf.poctask_queue.get()
        res = task["poc"].poc(task['host'], task['port'], conf.timeout)
        result_handler(task, res)


def result_handler(task, res):
    if not res:
        return
    logger.warning(f"{task['host']}:{task['port']} --> {res}")