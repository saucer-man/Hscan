import requests


def poc(host, port, timeout):
    try:
        r = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
        if "clusters" in r.text:
            return "jupyter is unauthorized"
    except:
        pass
    return None
