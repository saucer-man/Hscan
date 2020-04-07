import requests

def poc(host, port, timeout):
    try:
        # hadoop_YARN
        r = requests.get(f"http://{host}:{port}/cluster", timeout=timeout, allow_redirects=True, verify=False)
        if "Hadoop" in r.text:
            return "hadoop YARN is unauthorized"
    except:
        pass
    try:
        # hadoop_HDFS
        r = requests.get(f"http://{host}:{port}/explorer.html#/", timeout=timeout, allow_redirects=True, verify=False)
        if "Browse Directory" in r.text:
            return "hadoop HDFS is unauthorized"
    except:
        # print(host)
        pass
    return None


