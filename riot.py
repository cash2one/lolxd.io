import requests
import config


API_KEY = config.API_KEY
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


def base_request(query, region, static=False, **kwargs):
    """Make a request to the Riot API."""
    params = {'api_key': API_KEY}
    for key, value in kwargs.items():
        params[key] = value
    proxy = 'global' if static else region
    url = f'https://{proxy}.api.pvp.net/{query}'
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


def api_request(region, version, query):
    url = f'api/lol/{region}/{version}/{query}'
    return base_request(url, region)


def observer_mode_request(region, query):
    url = f'observer-mode/rest/{query}'
    return base_request(url, region)


def get_summoner_id(region, summoner_name, version='v1.4'):
    """Return the corresponding summoner ID."""
    query = f'summoner/by-name/{summoner_name}'
    r = api_request(region, version, query)
    return r[summoner_name.lower()]['id']


def get_ranked_stats(region, summoner_name, version='v1.3'):
    """Return the ranked stats of summoner_name."""
    summoner_id = get_summoner_id(region, summoner_name)
    query = f'stats/by-summoner/{summoner_id}/ranked'
    return api_request(region, version, query)


def get_current_game(region, summoner_name):
    """Return the information on *summoner_name*s current game."""
    summoner_id = get_summoner_id(region, summoner_name)
    platform_id = platforms[region]
    query = f'consumer/getSpectatorGameInfo/{platform_id}/{summoner_id}'
    return observer_mode_request(region, query)
