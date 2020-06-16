import requests


def poc(host, port, timeout):
    try:
        payload = f"http://{host}:{port}/manage"
        r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
        if "genkins" in r.text:
            return "genkins is unauthorized"
    except:
        # traceback.print_exc()
        pass
    return None
