# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 可参考文章 https://xz.aliyun.com/t/6103
from gevent import monkey
monkey.patch_all()
import sys
import gevent
import socket
import requests
import re
import binascii
from lib.common import color_print
from ftplib import FTP
try:
    from smb.SMBConnection import SMBConnection
except:
    color_print.red("[-] smb module not found! \n[-] try: pip install pysmb ")
    sys.exit()
# import traceback
timeout = 5


def redis(host, ports=[6379]):
    color_print.white("[*] redis未授权访问测试开始")
    socket.setdefaulttimeout(timeout)
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    for port in ports:
        try:
            s = socket.socket()
            s.connect((host, port))
            s.send(payload.encode('utf-8'))
            recv_data = s.recv(1024)
            s.close()
            if recv_data and b'redis_version' in recv_data:
                color_print.red(f'[+] redis未授权访问：{host}:{port}')
        except:
            # traceback.print_exc()
            pass


def mongo(host, ports=[27017]):
    color_print.white("[*] mongodb未授权访问测试开始")
    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex(
        "430000000300000000000000d40700000000000061646d696e2e24636d640000000000ffffffff1c000000016c69737444617461626173657300000000000000f03f00")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(payload)
            recv_data = s.recv(500)
            if "databases".encode('utf-8') in recv_data:
                color_print.red(f"[+] mongodb未授权访问：{host}:{port}")
        except:
            # traceback.print_exc()
            pass


def genkins(host, ports=[8080]):
    color_print.white("[*] genkins未授权访问测试开始")
    for port in ports:
        try:
            payload = f"http://{host}:{port}/manage"
            r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
            if "genkins" in r.text:
                color_print.red(f"[+] genkins未授权访问：{payload}")
        except:
            # traceback.print_exc()
            pass


def memcached(host, ports=[11211]):
    color_print.white("[*] memcached未授权访问测试开始")
    socket.setdefaulttimeout(timeout)
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("stats\r\n".encode())
            recv_data = s.recv(1024)
            s.close()
            if recv_data and b"STAT version" in recv_data:
                color_print.red(f"[+] memcached未授权访问：{host}:{port}")
        except:
            # traceback.print_exc()
            pass


def jboss(host, ports=[8080]):
    color_print.white("[*] jboss未授权访问测试开始")
    for port in ports:
        try:
            payload = f"http://{host}:{port}/jmx-console/"
            r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
            if "jboss" in r.text:
                color_print.red(f"jboss: {payload}")
        except:
            # traceback.print_exc()
            pass


def zookeeper(host, ports=[2181]):
    color_print.white("[*] zookeeper未授权访问测试开始")
    socket.setdefaulttimeout(timeout)
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("envi".encode())
            recv_data = s.recv(1024)
            s.close()
            if b'Environment' in recv_data:
                color_print.red(f"[+] zookeeper未授权访问：{host}:{port}")
        except:
            pass


def rsync(host, ports=[873]):
    color_print.white("[*] rsync未授权访问测试开始")
    # 代码参考https://raw.githubusercontent.com/ysrc/xunfeng/master/vulscan/vuldb/rsync_weak_auth.py
    def _rsync_init(host, port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        s.connect((host, port))
        s.send("@RSYNCD: 31\n".encode())
        _ = s.recv(1024)
        return s

    for port in ports:
        try:
            # 获取目录
            s = _rsync_init(host, port)
            s.send(bytes.fromhex('0a'))
            recv_data = s.recv(1024)
            s.close()
            paths = []
            if recv_data:
                for path_name in re.split('\n', recv_data.decode()):
                    if path_name and not path_name.startswith('@RSYNCD: '):
                        paths.append(path_name.split('\t')[0].strip())
            if paths:
                color_print.green(f"[+] 检测到rsync服务：{host}:{port}")
            # print(f"获取目录字节-----{recv_data}")
            # print(f"获取到的目录为-----------{paths}")

            # 尝试看下是否可以未授权访问
            for path in paths:
                s = _rsync_init(host, port)
                s.send(f"{path}\n".encode())
                recv_data = s.recv(1024)
                # print(f"尝试未授权访问接受的字节-----------{recv_data}")

                if recv_data.decode() == '\n':
                    recv_data = s.recv(1024)
                # 以下说明是未授权访问
                if recv_data.decode().startswith('@RSYNCD: OK'):
                    color_print.red(f"[+] rsync未授权访问：{host}:{port}/{path}")
                s.close()

        except:
            # traceback.print_exc()
            pass


def couchdb(host, ports=[5984]):
    color_print.white("[*] couchdb未授权访问测试开始")
    for port in ports:
        try:
            url = f"http://{host}:{port}"
            r = requests.get(url, timeout=timeout, allow_redirects=True, verify=False)
            if "couchdb" in r.text:
                color_print.red(f"[+] couchdb未授权访问：{host}:{port}")
        except:
            pass


def elasticsearch(host, ports=[9200]):
    color_print.white("[*] elasticsearch未授权访问测试开始")
    for port in ports:
        try:
            r = requests.get(f"http://{host}:{port}", timeout=timeout, allow_redirects=False, verify=False)
            if "You Know, for Search" in r.text:
                color_print.red(f"[+] elasticsearch未授权访问：{host}:{port}")
        except:
            pass  # traceback.print_exc()


def hadoop(host, ports=[8088]):
    color_print.white("[*] hadoop未授权访问测试开始")
    for port in ports:
        try:
            r = requests.get(f"http://{host}:{port}/cluster", timeout=timeout, allow_redirects=True, verify=False)
            if "Hadoop" in r.text:
                color_print.red(f"[+] hadoop未授权访问：{host}:{port}")
        except:
            pass


def jupyter(host, ports=[8888]):
    color_print.white("[*] jupyter未授权访问测试开始")
    for port in ports:
        try:
            r = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
            if "clusters" in r.text:
                color_print.red(f"[+] jupyter未授权访问：{host}:{port}")
        except:
            pass


def ftp(host, ports=[21]):
    color_print.white("[*] ftp未授权访问测试开始")
    for port in ports:
        try:
            ftp = FTP()
            ftp.connect(host, port)
            color_print.green(f"[+] 检测到ftp服务：{host}:{port}")
            ftp.login('anonymous', 'guest@guest.com')
            color_print.red(f"[+] ftp可匿名访问：{host}:{port}")
            ftp.quit()
        except:
            pass


def docker(host, ports=[2375]):
    # exp: https://github.com/Tycx2ry/docker_api_vul
    color_print.white("[*] docker未授权访问测试开始")
    for port in ports:
        try:
            r = requests.get(f"http://{host}:{port}/version", timeout=timeout, verify=False)
            if "ApiVersion" in r.text:
                color_print.red(f"[+] docker未授权访问：{host}:{port}")
        except:
            pass


def smb(host, ports=[445]):
    color_print.white("[*] smb未授权访问测试开始")
    for port in ports:
        try:
            conn = SMBConnection("", "", "", "", use_ntlm_v2=True)
            if conn.connect(host, port, timeout=timeout):
                color_print.green(f"[*] 检测到smb服务：{host}:{port}")
                sharelist = conn.listShares()
                for i in sharelist:
                    try:
                        conn.listPath(i.name, "/")
                        color_print.red(f"[+] smb未授权目录：{host}:{port}/{i.name}")
                    except:
                        color_print.green(f"[*] smb目录：{host}:{port}/{i.name}")

            conn.close()
        except:
            pass


def poc(host, ports):
    poc_list = ['redis', 'mongo', 'genkins', 'memcached', 'jboss', 'zookeeper', 'rsync', 'couchdb', \
                'elasticsearch', 'hadoop', 'jupyter', 'docker', 'ftp', 'smb']
    if ports:
        jobs = [gevent.spawn(globals()[p], host, ports) for p in poc_list]
    else:
        jobs = [gevent.spawn(globals()[p], host) for p in poc_list]

    gevent.joinall(jobs)