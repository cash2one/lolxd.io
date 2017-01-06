# -*- coding: utf-8 -*-
"""
    lolxd.champion_gg.py
    ~~~~~~~~~~~~~~~~~~~~

    This module contacts the Champion.gg API.
    Found at http://api.champion.gg/

    :copyright: (c) 2016 by Mads Damgaard and Carl Bordum Hansen.
    :license: MIT, see LICENSE for more details.
"""

import config
import requests
import riot
from functools import lru_cache

API_KEY = config.CHAMPION_GG_API_KEY


def api_call(query):
    """Request the json object of a call to the API.

    :rtype: dict
    """
    url = f'http://api.champion.gg/{query}?api_key={API_KEY}'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


@lru_cache()
def get_stats():
    """Query api for relevant stats for all champions.

    :rtype: a dictionary of dictionaries, relevant_stats:
        relevant_stats{
            name : str {
                deaths : double
                kills : double
                assists : double
                winrate : double
            }
            ...
        }
    :Usage:
        relevant_stats['name']['attribute'] # Returns the attribute of a champion with a given name
        relevant_stats['name'] # Returns all attributes for a champion with a given name
    """
    all_champions = api_call('stats')
    relevant_stats = {}

    for champion in all_champions:
        key = champion['name']
        relevant_stats[key] = {
            'deaths': champion['general']['deaths'],
            'kills': champion['general']['kills'],
            'assists': champion['general']['assists'],
            'winrate': champion['general']['winPercent']
        }
    return relevant_stats


def get_item_set(self):
    """
    Query the API for the most winning item set for the given champion

    :rtype: list of strings
    """
    url = f'champion/{self.champion_name}/items/finished/mostWins'
    items = api_call(url)[0]['items']
    item_names = [riot.get_item_name(item) for item in items]
    return item_names


def get_starting_items(self):
    """
    Query the API for the most popular starting items for the given champion

    :rtype list of strings
    """
    url = f'champion/{self.champion_name}/items/starters/mostPopular'
    items = api_call(url)[0]['items']
    item_names = [riot.get_item_name(item) for item in items]
    return item_names


def get_skill_order(self):
    """
    Query the API for the most popular skill order for the given champion

    :rtype list of strings
    """
    url = f'champion/{self.champion_name}/skills/mostPopular'
    return api_call(url)[0]['order']
