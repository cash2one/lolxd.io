import config
import requests

champion_API_KEY = config.champion_API_KEY


def api_call(query):
    """Return the json object of a call to the API."""
    url = f'http://api.champion.gg/{query}?api_key={champion_API_KEY}'
    r = requests.get(url)
    return r.json()


def get_all_champion_stats():
    """Return all stats for all champions."""
    return api_call('stats')


def get_item_set(champion_name):
    """Return a list of the most winning item set for a given champion."""
    url = f'champion/{champion_name}/items/finished/mostWins'
    return api_call(url)[0]['items']


def get_starting_items(champion_name):
    """Return a list of the most popular starting items for a given champion."""
    url = f'champion/{champion_name}/items/starters/mostPopular'
    return api_call(url)[0]['items']


def get_skill_order(champion_name):
    """Return a list of the most popular skill order for a given champion."""
    url = f'champion/{champion_name}/skills/mostPopular'
    return api_call(url)[0]['order']
