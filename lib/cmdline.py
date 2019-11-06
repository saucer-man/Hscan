#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file "LICENSE" for copying permission
"""
import argparse


def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    """
    parser = argparse.ArgumentParser(usage="python unauth.py -H 192.168.1.128")

    parser.add_argument("-H", "--host", help="scan target")
    parser.add_argument("-HF", "--host_file", help="scan target from file")
    parser.add_argument("-P", "--port", help="port to scan")
    parser.add_argument("-T", "--thread", type=int, help="num of thread")

    args = parser.parse_args()
    return args
