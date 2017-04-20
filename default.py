#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib2
from resources.lib.simpleplugin import Plugin
import string
import xbmc
import re

plugin = Plugin()

def build_anime_list(animes):
    animes_list = []
    for anime in animes:
        image = "https://punchsub.zlx.com.br/imagens/projetos/animes/%s.jpg" % (anime[0])
        animes_list.append({
            'label': anime[1],
            'url': plugin.get_url(action='view', name=anime[1], id=anime[0]),
            'thumb': image,
            'icon': image,
            'poster': image
        })
    return Plugin.create_listing(animes_list, content="tvshows",  view_mode=500)

@plugin.mem_cached(1440)
def login():
    url = "https://punchsub.zlx.com.br/login"

    username = plugin.get_setting("username")
    password = plugin.get_setting("password")

    payload = "login=%s&senha=%s&B1=Entrar" % (username, password)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }

    session = requests.Session()
    session.request("POST", url, data=payload, headers=headers)
    return session.cookies


@plugin.mem_cached(30)
def get_animes():
    return requests.get('https://punchsub.zlx.com.br/lista-de-animes').json()

@plugin.mem_cached(30)
def get_episodes(id):
    url = ('https://punchsub.zlx.com.br/listar/%s/episodios/hd' % (id))
    return requests.get(url).json()

@plugin.action()
def root():
    return [{
                'label': "Últimos Lançamentos",
                'url': plugin.get_url(action='latest')
            },
            {
                'label': "Todos",
                'url': plugin.get_url(action='list_all')
            },
            {
                'label': "Por Letra",
                'url': plugin.get_url(action='letters')
            }
        ]

@plugin.action()
def latest():
    animes = sorted(get_animes(), key=lambda k: k[9], reverse=True)
    return build_anime_list(animes[0:29])

@plugin.action()
def list_by_letter(params):
    animes = get_animes()

    filtered = filter(lambda k: re.match(params.match, k[1].upper()), animes)
    return build_anime_list(filtered)

@plugin.action()
def list_all():
    animes = get_animes()

    return build_anime_list(animes)

@plugin.action()
def letters():
    matches = list(string.ascii_uppercase)

    letters = [{
                'label': "#",
                'url': plugin.get_url(action='list_by_letter', match="^[0-9]")
            }]

    for m in matches:
        letters.append({
                'label': m,
                'url': plugin.get_url(action='list_by_letter', match="^"+m)
            })

    return letters

@plugin.action()
def view(params):
    episodes = get_episodes(params.id)

    episodes_list = []
    for episode in episodes["e"]:
        id = episode[0]
        number = episode[1]
        slug = episodes["p"][9]

        episodes_list.append({
            'label': "Episódio {}".format(number),
            'thumb': "https://punchsub.zlx.com.br/imagens/projetos/screens/%s_%s.jpg" % (params.id, episode[2]),
            'url': plugin.get_url(action='play', id=id, slug=slug, number=number),
            'is_playable': True
        })

    return episodes_list

@plugin.action()
def play(params):
    cookies = login()

    resp = requests.post("https://punchsub.zlx.com.br/lista-episodios", cookies=cookies, data=[('ids[]', params.id)]).json()
    download_number = resp[params.id]["versao"].split("/")[1]

    url = "http://vip-validation2.punchsub.net/vip/vipDlRedir_1.php?downNum=%s&slug=%s-%s-hd&t=e" % (download_number, params.slug, params.number)

    return url

if __name__ == '__main__':
    plugin.run()  # Start plugin
