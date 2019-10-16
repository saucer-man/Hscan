from lib.common import getip, color_print
from lib.poc import poc


if __name__ == "__main__":
    target = input("[*] 请输入检测目标:")
    ip_list = getip(target)
    color_print.cyan(f"[+] 将要检测以下目标: {ip_list}")
    ports = input("[*] 请输入目标开放的端口(可为空):")
    ports = [int(i.strip()) for i in ports.split(",") if i]
    if ports:
        color_print.cyan(f"[+] 将会检测以下端口: {ports}")
    else:
        color_print.cyan(f"[+] 将会检测默认端口")
    for ip in ip_list:
        poc(ip, ports)