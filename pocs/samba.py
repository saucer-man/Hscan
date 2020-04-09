from smb.SMBConnection import SMBConnection


# bug --> https://github.com/miketeo/pysmb/blob/b5b4012be9090c0bba4556a8fb95401937e98528/python3/nmb/base.py#L84

def poc(host, port, timeout):
    # smb unauthorised
    try:
        conn = SMBConnection("", "", "", "", use_ntlm_v2=True)
        if conn.connect(host, port, timeout=timeout):
            unauth_path = []
            sharelist = conn.listShares()
            for i in sharelist:
                try:
                    conn.listPath(i.name, "/")
                    unauth_path.append(i.name)
                except:
                    pass
                #     return "smb directory"
            if len(unauth_path) > 0:
                return f"smb unauthorised: directory：{'/'.join(unauth_path)}"
            else:
                return "smb service detected"
        conn.close()
    except:
        pass
    return None