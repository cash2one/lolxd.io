# -*- coding: utf-8 -*-
"""
    lolxd.championgg.py
    ~~~~~~~~~~

    This module contacts the Champion.gg API.
    Found at http://api.champion.gg/

    :copyright: (c) 2016 by Mads Damgaard and Carl Bordum Hansen.
    :license: MIT, see LICENSE for more details.
"""

import config
import requests
import riot

API_KEY = config.CHAMPION_API_KEY

def api_call(query):
    """Reqeust the json object of a call to the API.

    :rtype dict
    """
    url = f'http://api.champion.gg/{query}?api_key={API_KEY}'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_all_champion_stats():
    """Query api for all stats for all champions.

    :rtype linked dicts
    """
    return api_call('stats')


class Summoner:


    def __init__(self, champion_name):
        """
            Initialize an instance of *Summoner* with a champion name
        """
        self.champion_name = champion_name


    def get_item_set(self):
        """
        Query the API for the most winning item set for the given champion

        :rtype list of strings
        """
        url = f'champion/{self.champion_name}/items/finished/mostWins'
        items = api_call(url)[0]['items']
        item_name = [riot.get_item_name(item) for item in items]
        return(item_name)


    def get_starting_items(self):
        """
        Query the API for the most popular starting items for the given champion

        :rtype list of strings
        """
        url = f'champion/{self.champion_name}/items/starters/mostPopular'
        items = api_call(url)[0]['items']
        item_names = [riot.get_item_name(item) for item in items]
        return(item_names)


    def get_skill_order(self):
        """
        Query the API for the most popular skill order for the given champion

        :rtype list of strings
        """
        url = f'champion/{self.champion_name}/skills/mostPopular'
        return api_call(url)[0]['order']
