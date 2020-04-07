import requests


def poc(host, port, timeout):
    # exp: https://github.com/Tycx2ry/docker_api_vul
    try:
        r = requests.get(f"http://{host}:{port}/version", timeout=timeout, verify=False)
        if "ApiVersion" in r.text:
            return "docker remote api is unauthorized"
    except:
        pass
    # docker_register 未授权
    # exp: https://github.com/NotSoSecure/docker_fetch
    try:
        r = requests.get(f"http://{host}:{port}/v2/_catalog", timeout=timeout, verify=False)
        if "repositories" in r.text:
            return "docker Registry API is unauthorized"
    except:
        pass

    try:
        r = requests.get(f"http://{host}:{port}/v1/_catalog", timeout=timeout, verify=False)
        if "repositories" in r.text:
            return "docker Registry API is unauthorized"
    except:
        pass
    return None