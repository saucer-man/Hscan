import requests



def poc(host, port, timeout):
    try:
        url = f"http://{host}:{port}"
        r = requests.get(url, timeout=timeout, allow_redirects=True, verify=False)
        if "couchdb" in r.text:
            return "couchdb is unauthorized"
    except:
        pass