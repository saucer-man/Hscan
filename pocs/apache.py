import requests

def poc(host, port, timeout):
    try:
        # Apache_Flink
        # print(f"http://{host}:{port}/jar/upload")
        res = requests.get(f"http://{host}:{port}", timeout=timeout, verify=False)
        if"apache flink" in res.text.lower():
            return "Apache_Flink upload file to rce"
    except Exception as e:
        pass
    return None