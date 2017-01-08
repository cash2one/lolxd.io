
"""
    lolxd.riot
    ~~~~~~~~~~

    This module contacts the official League of Legends API.

    :copyright: (c) 2016 by Mads Damgaard and Carl Bordum Hansen.
    :license: MIT, see LICENSE for more details.
"""
from functools import lru_cache
import itertools
import requests
import config


API_KEY = config.RIOT_API_KEY

platforms = {
    'br': 'BR1',
    'eune': 'EUN1',
    'euw': 'EUW1',
    'kr': 'KR',
    'lan': 'LA1',
    'las': 'LA2',
    'na': 'NA1',
    'oce': 'OC1',
    'ru': 'RU',
    'tr': 'TR1',
    'jp': 'JP1'
}

keystone_ids = (6161, 6162, 6164, 6361, 6362, 6363, 6261, 6262, 6263)
# region_cycle = itertools.cycle(platforms.keys())


def base_request(query, proxy, **kwargs):
    """Make a request to the Riot API.

    :rtype: dict
    """
    params = {'api_key': API_KEY}
    for key, value in kwargs.items():
        params[key] = value
    url = f'https://{proxy}.api.pvp.net/{query}'
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


def api_request(region, version, query):
    """Make a request to the RIOT API at the URL '/api/lol/'.

    :rtype: dict
    """
    url = f'api/lol/{region}/{version}/{query}'
    return base_request(url, region)


def observer_mode_request(region, query):
    """Make a request to the Riot API at the URL '/observer-mode/rest/'.

    :rtype: dict
    """
    url = f'observer-mode/rest/{query}'
    return base_request(url, region)


@lru_cache()
def static_request(query, version):
    """Make a request to lol-static-data. The results are stored.

    These requests does not count against your rate limit.

    :rtype: dict
    """
    region = 'euw'  # next(region_cycle)
    return base_request(f'api/lol/static-data/{region}/{version}/{query}', 'global')


def get_summoner_id(region, summoner_name, version='v1.4'):
    """Return the corresponding summoner ID.

    :rtype: int
    """
    query = f'summoner/by-name/{summoner_name}'
    r = api_request(region, version, query)
    return r[summoner_name.lower()]['id']


def get_ranked_stats(region, summoner_id, version='v1.3'):
    """Return the ranked stats of summoner_id

    :rtype: dict
    """
    query = f'stats/by-summoner/{summoner_id}/ranked'
    return api_request(region, version, query)


def get_current_game(region, summoner_id):
    """Return all available information on current game.

    :rtype: dict
    """
    platform_id = platforms[region]
    query = f'consumer/getSpectatorGameInfo/{platform_id}/{summoner_id}'
    return observer_mode_request(region, query)


def get_item_name(item_id, version='v1.2'):
    """Return the name of an item. This is a <static request>.

    :rtype: str
    """
    return static_request(f'item/{item_id}', version)['name']


def get_champion_name(champion_id, version='v1.2'):
    """Return the name of a champion. This is a <static request>.

    :rtype: str
    """
    return static_request(f'champion/{champion_id}', version)['name']


def get_champion_key(champion_id, version='v1.2'):
    """Return the key of a champion. This is a <static request>.

    :rtype: str
    """
    return static_request(f'champion/{champion_id}', version)['key']


def get_summoner_spell_key(spell_id, version='v1.2'):
    """Return the name of a summoner spell. This is a <static request>.

    :rtype: str
    """
    return static_request(f'summoner-spell/{spell_id}', version)['key']


def get_keystone_id(iterable_of_masteries):
    """Return the id of the keystone mastery in an iterable of masteries.

    Each mastery should be a dictionary with the keys 'masteryId' and 'rank'.
    """
    for mastery in iterable_of_masteries:
        if mastery['masteryId'] in keystone_ids:
            return mastery['masteryId']


def get_ranking(region, list_of_ids):
    """Return a dict with each id in *list_of_ids* as keys, and a tuple of (tier, division) as value.

    Example tuple = ('DIAMOND', 'III')

    :rtype: dict
    """
    ids = ','.join([str(elem) for elem in list_of_ids])
    r = api_request(region, 'v2.5', f'league/by-summoner/{ids}/entry')
    int_keys = [int(key) for key in r.keys()]
    ranking_dict = {}
    for ID in list_of_ids:
        tier = 'PROVISIONAL'
        division = 'I'
        if ID in int_keys:
            tier = r[str(ID)][0]['tier']
            division = r[str(ID)][0]['entries'][0]['division']
        ranking_dict[ID] = (tier, division)
    return ranking_dict


def get_previous_tiers(region, match_id):
    """Return a dict with player id as key and previous season tier as value."""
    r = api_request(region, 'v2.2', f'match/{match_id}')
    return {player['participantId']: player['highestAchievedSeasonTier'] for player in r['participants']}
