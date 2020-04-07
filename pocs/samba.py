from smb.SMBConnection import SMBConnection


def poc(host, port, timeout):
    # smb未授权访问
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