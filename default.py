#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib2
from resources.lib.simpleplugin import Plugin
from punch import Punch
import string
import xbmc
import re

plugin = Plugin()
punch = Punch(plugin.get_setting("username"), plugin.get_setting("password"))

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

# @plugin.mem_cached(1440)
def login():
    return punch.login()

@plugin.mem_cached(30)
def get_animes():
    return punch.get_animes()

@plugin.mem_cached(30)
def get_episodes(id):
    return punch.get_episodes(id)

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
    animes = punch.get_animes()

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
    episodes = punch.get_episodes(params.id)

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
    return punch.get_playable_url({"id": params.id, "slug": params.slug, "number": params.number})

if __name__ == '__main__':
    plugin.run()  # Start plugin
