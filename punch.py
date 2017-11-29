#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def login():
    url = "https://punchsub.com/login"


    payload = "login=%s&senha=%s&B1=Entrar&page=%s" % (username, password, "https://punchsub.com/principal")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }

    session = requests.Session()
    resp = session.request("POST", url, data=payload, headers=headers)
    print "login header", resp.headers
    print "login resp", resp.text

    return session.cookies


if __name__ == '__main__':
    cookies = login()

    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        'content-type': "application/x-www-form-urlencoded",
    }

    payload = "ids[]=67183"
    resp = requests.post("https://punchsub.com/lista-episodios", headers=headers, cookies=cookies, data=payload)
    down_link = "https://punchsub.com/%s/%s-%s-hd" % (resp.json()["67183"]["versao"], "shokugeki-no-souma-ni-no-sara-ova", "2")
    resp = requests.get(down_link, headers=headers, cookies=cookies, allow_redirects=False)
    print resp.status_code
    print resp.headers["Location"]

    print "resp => ", resp.text
