"""
    lolxd.champion_gg.py
    ~~~~~~~~~~~~~~~~~~~~

    This module contacts the Champion.gg API.
    Found at http://api.champion.gg/

    :author: Mads Damgaard Pedersen
    :copyright: (c) 2016 by Mads Damgaard Pedersen and Carl Bordum Hansen.
    :license: MIT, see LICENSE for more details.
"""

import config
import requests
from functools import lru_cache

API_KEY = config.CHAMPION_GG_API_KEY

def api_call(query):
    """Return json object of a call to the API.

    :param query: string containing the necessary elements to complete the URL
    :rtype: dict
    """
    url = f'http://api.champion.gg/{query}?api_key={API_KEY}'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


@lru_cache()
def get_stats():
    """Return relevant stats for all champions.

    :usage:
    relevant_stats['name']['attribute'] # Returns the 'attribute' of a champion with a given 'name'
    relevant_stats['name'] # Returns all attributes for a champion with a given 'name'

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


@lru_cache()
def get_item_set(champion_name):
    """
    Return the most winning item set for the given champion.

    :param champion_name: name of a champion
    :rtype: list of strings
    """
    url = f'champion/{champion_name}/items/finished/mostWins'
    items = api_call(url)[0]['items']
    # item_names = [riot.get_item_name(item) for item in items]
    return items


@lru_cache()
def get_starting_items(champion_key):
    """
    Return the most winning starting items for the given champion.

    :param champion_key: the key corresponding to a champion
    :rtype: list of strings
    """
    url = f'champion/{champion_key}/items/starters/mostWins'
    items = api_call(url)[0]['items']
    # item_names = [riot.get_item_name(item) for item in items]
    return items


@lru_cache()
def get_skill_order(champion_key):
    """
    Return the most winning skill order for the given champion.

    :param champion_key: the key corresponding to a champion
    :rtype: list of strings
    """
    url = f'champion/{champion_key}/skills/mostWins'
    return api_call(url)[0]['order']
