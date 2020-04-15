import requests

# refer https://xz.aliyun.com/t/2233
# https://github.com/rabbitmask/SB-Actuator/blob/master/SB-Actuator.py
# Spring Boot < 1.5 默认未授权访问所有端点
# Spring Boot >= 1.5 默认只允许访问/health和/info端点，但是此安全性通常被应用程序开发人员禁用
# 另外考虑到人为关闭默认端点开启非默认端点的情况，综上所述，此处采用暴力模式配合异步并发（子进程中嵌套异步子线程）解决。


def poc(host, port, timeout):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", }
    pathlist = ['autoconfig', 'beans', 'env', 'configprops', 'dump', 'health', 'info', 'mappings', 'metrics',
                'shutdown', 'trace', ]

    for path in pathlist:
        # Spring Boot 1.x版本端点在根URL下注册。
        try:
            r = requests.get(f"http://{host}:{port}/{path}", headers=headers, timeout=timeout, verify=False)
            if r.status_code == 200:
                return f"springBoot actuator is unauthorized: http://{host}:{port}/{path}"
        except:
            pass
        # Spring Boot 2.x版本端点移动到/actuator/路径。
        try:
            r = requests.get(f"http://{host}:{port}/actuator/{path}", headers=headers, timeout=timeout, verify=False)
            if r.status_code == 200:
                return f"springBoot actuator is unauthorized: http://{host}:{port}/actuator/{path}"
        except:
            pass
    # 大多数Actuator仅支持GET请求并仅显示敏感的配置数据,如果使用了Jolokia端点，可能会产生XXE、甚至是RCE安全问题。
    # 通过查看/jolokia/list 中存在的 Mbeans，是否存在logback 库提供的reloadByURL方法来进行判断。
    try:
        r = requests.get(f"http://{host}:{port}/jolokia/list", headers=headers, timeout=timeout, verify=False)
        if r.status_code == 200:
            if 'reloadByURL' in r.text:
                return "spring jolokia 端点未授权，可进行XXE/RCE测试"
            return "spring jolokia 端点未授权"
    except:
        pass
    return None