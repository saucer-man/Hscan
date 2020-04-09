import requests

# refer https://xz.aliyun.com/t/2233


def poc(host, port, timeout):
    try:
        res = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
        if"node exporter" in res.text.lower():
            return "springBoot actuator is unauthorized"
    except:
        pass
    return None