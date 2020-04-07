import requests


def poc(host, port, timeout):
    try:
        payload = f"http://{host}:{port}/jmx-console/"
        r = requests.get(payload, timeout=timeout, allow_redirects=False, verify=False)
        if "jboss" in r.text:
            return "jboss is unauthorized"
    except:
        # traceback.print_exc()
        pass
    return None