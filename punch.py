#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from fuzzywuzzy import fuzz

class LoginError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Punch:
    def __init__(self, username, password):
        self.base_url = "https://punchsub.com/"
        self.cookies = None
        self.username = username
        self.password = password

    def login(self):
        if not self.username or not self.password:
            raise LoginError("username or password undefined")

        url = self.base_url+"/login"

        payload = "login=%s&senha=%s&B1=Entrar&page=%s" % (self.username, self.password, "https://punchsub.com/principal")
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
            }

        session = requests.Session()
        session.request("POST", url, data=payload, headers=headers)
        return session.cookies

    def get_animes(self):
        return requests.get(self.base_url+'/lista-de-animes').json()

    def search_anime(self, query):
        animes = self.get_animes()
        closest = None
        max_ratio = 0
        for anime in animes:
            title = anime[1].lower()
            ratio = fuzz.token_sort_ratio(query.lower(), title)
            if ratio > max_ratio:
                max_ratio = ratio
                closest = anime

        return closest

    def get_episodes(self, id):
        url = '%s/listar/%s/episodios/hd' % (self.base_url, id)
        return requests.get(url).json()

    def get_playable_url(self, params):
        if not self.cookies:
            self.cookies = self.login()

        headers = {
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
            'content-type': "application/x-www-form-urlencoded",
        }

        payload = "ids[]="+params["id"]
        resp = requests.post("https://punchsub.com/lista-episodios", headers=headers, cookies=self.cookies, data=payload)

        if resp.text == "":
            self.cookies = None
            return self.get_playable_url(params)

        down_link = "https://punchsub.com/%s/%s-%s-hd" % (resp.json()[params["id"]]["versao"], params["slug"], params["number"])
        resp = requests.get(down_link, headers=headers, cookies=self.cookies, allow_redirects=False)

        return resp.headers["Location"]

if __name__ == '__main__':
    punch = Punch("test", "test")
    print punch.search_anime("Boruto: Naruto Next Generations")

