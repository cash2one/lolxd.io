import json
import requests
import config


API_KEY = config.API_KEY
URL = 'https://euw.api.pvp.net/api/lol/{region}/{version}/{query}'
LIVE_URL = 'https://euw.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{}/{}?api_key=' + API_KEY


def api_call(region, version, query):
    path = URL.format(region=region, version=version, query=query)
    return requests.get(path, params={'api_key': API_KEY})


def get_summoner_id(region, summoner_name):
    r = api_call(region, 'v1.4', 'summoner/by-name/{}'.format(summoner_name))
    return json.loads(r.text)[summoner_name.lower()]['id']


def get_ranked_stats(region, summoner_name):
    summoner_id = get_summoner_id(region, summoner_name)
    return json.loads(api_call(region, 'v1.3', 'stats/by-summoner/{}/ranked'.format(summoner_id)).text)


def get_current_game(region, platform_id, summoner_name):
    summoner_id = get_summoner_id(region, summoner_name)
    query = LIVE_URL.format(platform_id, summoner_id)
    return json.loads(requests.get(query).text)


print(json.dumps(get_current_game('euw', 'EUW1', 'Phanda'), indent=4))