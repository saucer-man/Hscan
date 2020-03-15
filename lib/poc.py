# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# reference https://xz.aliyun.com/t/6103

import sys
import socket
import requests
import re
import json
import binascii
import traceback
import urllib3
from lib.common import color_print
from ftplib import FTP
try:
    from smb.SMBConnection import SMBConnection
    import pymysql
    # import cx_Oracle
    # import psycopg2
except:
    color_print.red("[-]  module not found! \n[-] try: pip install -r requirement.txt ")
    sys.exit()


urllib3.disable_warnings()
timeout = 3


def redis(host, port=6379):
    socket.setdefaulttimeout(timeout)
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(payload.encode('utf-8'))
        recv_data = s.recv(1024)
        s.close()
        if recv_data and b'redis_version' in recv_data:
            color_print.red(f'[+] redis is not authorized to access：{host}:{port}')
        elif b'NOAUTH Authentication required' in recv_data:
            color_print.green(f'[+] redis service detected (authorization required)：{host}:{port}')
        elif b"protected mode is enabled" in recv_data:
            color_print.green(f'[+] redis service detected (running in protected mode)：{host}:{port}')
    except:
        # traceback.print_exc()
        pass


def mongo(host, port=27017):
    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex(
        "430000000300000000000000d40700000000000061646d696e2e24636d640000000000ffffffff1c000000016c69737444617461626173657300000000000000f03f00")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(payload)
        recv_data = s.recv(1024)
        if b"databases"in recv_data:
            color_print.red(f"[+] mongodb is not authorized to access：{host}:{port}")
        if b"Unauthorized" in recv_data:
            color_print.green(f"[+] mongodb service detected (authorization required)：{host}:{port}")
    except:
        # traceback.print_exc()
        pass


def genkins(host, port=8080):
    try:
        payload = f"http://{host}:{port}/manage"
        r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
        if "genkins" in r.text:
            color_print.red(f"[+] genkins is not authorized to access：{payload}")
    except:
        # traceback.print_exc()
        pass


def memcached(host, port=11211):
    socket.setdefaulttimeout(timeout)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("stats\r\n".encode())
        recv_data = s.recv(1024)
        s.close()
        if recv_data and b"STAT pid" in recv_data:
            color_print.red(f"[+] memcached is not authorized to access：{host}:{port}")
    except:
        # traceback.print_exc()
        pass


def jboss(host, port=8080):
    try:
        payload = f"http://{host}:{port}/jmx-console/"
        r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
        if "jboss" in r.text:
            color_print.red(f"jboss is not authorized to access: {payload}")
    except:
        # traceback.print_exc()
        pass


def druid(host, port=80):
    druid_path = [f"http://{host}:{port}/druid/index.html", f"http://{host}:{port}/system/index.html",
                  f"http://{host}:{port}/webpage/system/druid/index.html"]
    for path in druid_path:
        try:
            r = requests.get(path, timeout=timeout, allow_redirects=False, verify=False)
            if "Druid Stat Index" in r.text:
                color_print.red(f"Druid is not authorized to access: {path}")
        except:
            # traceback.print_exc()
            pass

def zookeeper(host, port=2181):
    socket.setdefaulttimeout(timeout)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("envi".encode())
        recv_data = s.recv(1024)
        s.close()
        if b'zookeeper.version' in recv_data:
            color_print.red(f"[+] zookeeper is not authorized to access：{host}:{port}")
    except:
        pass


def rsync(host, port=873):
    # refer: https://raw.githubusercontent.com/ysrc/xunfeng/master/vulscan/vuldb/rsync_weak_auth.py
    def _rsync_init(host, port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        s.connect((host, port))
        s.send("@RSYNCD: 31\n".encode())
        _ = s.recv(1024)
        return s

    try:
        # get directory
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
            color_print.green(f"[+] detected rsync service：{host}:{port}")
        # print(f"get directory bytes-----{recv_data}")
        # print(f"The obtained directory is-----------{paths}")

        # Try to see if can gain unauthorized access
        for path in paths:
            s = _rsync_init(host, port)
            s.send(f"{path}\n".encode())
            recv_data = s.recv(1024)
            # print(f" Trying to grant unauthorized access to the accepted bytes-----------{recv_data}")

            if recv_data.decode() == '\n':
                recv_data = s.recv(1024)
            # The following instructions prove unauthorized access
            if recv_data.decode().startswith('@RSYNCD: OK'):
                color_print.red(f"[+] rsync is not authorized to access：{host}:{port}/{path}")
            s.close()

    except:
        # traceback.print_exc()
        pass


def couchdb(host, port=5984):
    try:
        url = f"http://{host}:{port}"
        r = requests.get(url, timeout=timeout, allow_redirects=True, verify=False)
        if "couchdb" in r.text:
            color_print.red(f"[+] couchdb is not authorized to access：{host}:{port}")
    except:
        pass


def elasticsearch(host, port=9200):
    try:
        r = requests.get(f"http://{host}:{port}", timeout=timeout, allow_redirects=False, verify=False)
        if "You Know, for Search" in r.text:
            if(elasticsearch_cve_2014_3120_rce_check(host, port)):
                color_print.red(f"[+] elasticsearch cve-2014-3120：{host}:{port}")
            if(elasticsearch_cve_2015_1427_rce_check(host, port)):
                color_print.red(f"[+] elasticsearch cve-2015-1427：{host}:{port}")
            if(elasticsearch_cve_2015_3337_rce_check(host, port)):
                color_print.red(f"[+] elasticsearch cve-2015-3337：{host}:{port}")
            else:
                color_print.red(f"[+] elasticsearch is not authorized to access：{host}:{port}")
    except:
        pass  # traceback.print_exc()


def elasticsearch_cve_2014_3120_rce_check(host, port=9200):
    data = '''{
    "size": 1,
    "query": {
      "filtered": {
        "query": {
          "match_all": {
          }
        }
      }
    },
    "script_fields": {
        "command": {
            "script": "37182379+74892374"
        }
    }
    }'''
    try:
        r = requests.post(f"http://{host}:{port}/_search?pretty", data=data, timeout=timeout)
        if r.status_code == 200 and '112074753' in r.text:
            return True
    except:
        pass
    return False


def elasticsearch_cve_2015_1427_rce_check(host, port=9200):
    data = '''{
    "size":1,
    "script_fields": {
       "secpulse": { "script":"372137931+31829038120",
       "lang": "groovy"
    }
  }
}}'''
    try:
        r = requests.post(f"http://{host}:{port}/_search?pretty", data=data, timeout=timeout)
        if r.status_code == 200 and '32201176051' in r.text:
            return True
    except:
        pass
    return False


def elasticsearch_cve_2015_3337_rce_check(host, port=9200):
    try:
        r = requests.get(f"http://{host}:{port}/_plugin/../../../../../../../../../../../etc/passwd")
        if r.status == 200 and 'root' in r.text:
            return True
    except:
        pass
    return False


def hadoop_YARN(host, port=8088):
    try:
        r = requests.get(f"http://{host}:{port}/cluster", timeout=timeout, allow_redirects=True, verify=False)
        if "Hadoop" in r.text:
            color_print.red(f"[+] hadoop YARN is not authorized to access：{host}:{port}")
    except:
        pass


def hadoop_HDFS(host, port=50070):
    try:
        r = requests.get(f"http://{host}:{port}/explorer.html#/", timeout=timeout, allow_redirects=True, verify=False)
        if "Browse Directory" in r.text:
            color_print.red(f"[+] hadoop HDFS is not authorized to access：{host}:{port}")
    except:
        # print(host)
        pass
        
def Apache_Flink(host, port=8081):
    try:
        # print(f"http://{host}:{port}/jar/upload")
        res = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
        if"apache flink" in res.text.lower():
            color_print.red(f"[+] Apache_Flink upload file to rce：{host}:{port}")
        else:
            pass
    except Exception as e:
        pass
        

def grafana(host, port=3000):
    try:
        headers={
        "Content-Type": "application/json;charset=UTF-8"
        }
        data = {"user": "admin", "email": "", "password": "admin"}
        res = requests.post(f"http://{host}:{port}/login", headers=headers, data=json.dumps(data), timeout=timeout, verify=False)
        if "Logged in" in res.text:
            color_print.red(f"[+] grafana weakpass admin/admin：{host}:{port}")
        else:
            res = requests.get(f"http://{host}:{port}")
            if "grafana.com" in res.text:
                color_print.green(f"[+] grafana service detected：{host}:{port}")
    except Exception as e:
        pass


def jupyter(host, port=8888):
    try:
        r = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
        if "clusters" in r.text:
            color_print.red(f"[+] jupyter is not authorized to access：{host}:{port}")
    except:
        pass


def ftp(host, port=21):
    try:
        ftp = FTP(timeout=timeout)
        ftp.connect(host, port)
        color_print.green(f"[+] ftp service detected：{host}:{port}")
        ftp.login('anonymous', 'guest@guest.com')
        color_print.red(f"[+] ftp is not authorized to access：{host}:{port}")
        ftp.quit()
    except:
        pass


def docker(host, port=2375):
    # exp: https://github.com/Tycx2ry/docker_api_vul
    try:
        r = requests.get(f"http://{host}:{port}/version", timeout=timeout, verify=False)
        if "ApiVersion" in r.text:
            color_print.red(f"[+] docker remote api is not authorized to access：{host}:{port}")
    except:
        pass


def docker_register(host, port=30000):
    # exp: https://github.com/NotSoSecure/docker_fetch
    try:
        r = requests.get(f"http://{host}:{port}/v2/_catalog", timeout=timeout, verify=False)
        if "repositories" in r.text:
            color_print.red(f"[+] docker Registry API is not authorized to access：{host}:{port}")
    except:
        pass
    try:
        r = requests.get(f"http://{host}:{port}/v1/_catalog", timeout=timeout, verify=False)
        if "repositories" in r.text:
            color_print.red(f"[+] docker Registry API is not authorized to access：{host}:{port}")
    except:
        pass


def smb(host, port=445):
    try:
        conn = SMBConnection("", "", "", "", use_ntlm_v2=True)
        if conn.connect(host, port, timeout=timeout):
            color_print.green(f"[*] smb service detected：{host}:{port}")
            sharelist = conn.listShares()
            for i in sharelist:
                try:
                    conn.listPath(i.name, "/")
                    color_print.red(f"[+] smb unauthorised directory：{host}:{port}/{i.name}")
                except:
                    color_print.green(f"[*] smb directory：{host}:{port}/{i.name}")

        conn.close()
    except:
        pass


def postgresql(host, port=5432):
    # try:
    #     conn = psycopg2.connect(host=host, port=port, database="postgres",
    #                             user="postgres", password="123456", connect_timeout=timeout)
    #     conn.close()
    #     color_print.red(f"[+] postgresql is not authorized：{host}:{port}:postgres：123456")
    # except:
    #     if "no pg_hba.conf entry" in traceback.format_exc():
    #         color_print.green(f"[+] postgresql service detected (local login only)：{host}:{port}")

    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex("00000029000300007573657200706f73746772657300646174616261736500706f7374677265730000")
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(payload)
        recv_data = s.recv(1024)
        s.close()
        # print(binascii.b2a_hex(recv_data))
        # no pg_hba.conf
        if b"70675f6862612e636f6e66" in binascii.b2a_hex(recv_data):
            color_print.green(f"[+] postgresql service detected (local login only)：{host}:{port}:postgres")
        # R
        elif binascii.b2a_hex(recv_data).startswith(b"520000000c0000000"):
            color_print.green(f"[+] postgresql service detected (need password)：{host}:{port}:postgres")
        # server_version
        elif b"7365727665725f76657273696f6e" in binascii.b2a_hex(recv_data):
            color_print.red(f"[+] postgresql is not authorized：{host}:{port}:postgres")
    except:
        # traceback.print_exc()
        pass
    # color_print.white(f"postgresql done")


# def oracle(host, port=1521):
#     try:
#         conn = cx_Oracle.connect("scott/tiger@" + host + ":" + str(port) + "/orcl", timeout=timeout)
#         conn.close()
#         color_print.red(f"[+] oracle weak password：{host}:{port}:scott:tiger")
#     except:
#         if "Cannot locate a 64-bit Oracle Client library" in traceback.format_exc():
#             color_print.red(f"[-] Oracle Instant Client not installed --> Oracle Instant Client")
#         elif "the account is locked" in traceback.format_exc():
#             color_print.green(f"[+] oracle service detected：{host}:{port}")
#     # color_print.white(f"oracle done")


def mysql(host, port=3306):
    try:
        conn = pymysql.connect(host=host, port=port, user="root", password="123456",
                               db='mysql', connect_timeout=timeout, read_timeout=timeout, write_timeout=timeout)
        conn.close()
        color_print.red(f"[+] mysql weak password：{host}:{port}:root:123456")
    except:
        #print(traceback.format_exc())
        if "Access denied for user" in traceback.format_exc():
            color_print.green(f"[+] detected mysql service：{host}:{port}")


def mssql(host, port=1433):
    socket.setdefaulttimeout(timeout)
    payload = binascii.a2b_hex("1001010400000000fc00000001000071001000000683f2f8602e000000000000e001000088ffffff3604000056000d00700002007400090086000d00a000140000000000c8000a00dc000a00f0000600000000000000fc000000fc00000059005400530048004c005400310039003000360030003200370073006100b0a5d2a5f3a5b6a586a596a5e6a5f6a5c6a5700079006d007300730071006c003d0032002e0031002e0034003100390032002e003100360038002e003100330036002e003100320038003a003100340033003300440042002d004c00690062007200610072007900750073005f0065006e0067006c006900730068006d0061007300740065007200")
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(payload)
        recv_data = s.recv(1024)
        s.close()
        # print(binascii.b2a_hex(recv_data))
        # master
        if b"6d00610073007400650072" in binascii.b2a_hex(recv_data):
            color_print.red(f"[+] mssql weak password：{host}:{port}:sa:Qwe123456")
        # Login failed
        elif b"27007300610027" in binascii.b2a_hex(recv_data):
            color_print.green(f"[+] detected mssql service：{host}:{port}")
    except:
        # traceback.print_exc()
        pass




