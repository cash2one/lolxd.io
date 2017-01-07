from flask import Flask, render_template
import riot
import champion_gg
import itertools


app = Flask(__name__)


def percentage(a, b):
    """Return a 1 point decimal float representing a% of a + b."""
    return round(a / (a + b) * 100, 1)


def get_teams(region, summoner_name):
    """Return two lists representing the players on blue and red team respectively.

    A player dictionary looks like this:
        player {
            summoner_name : str
            tier : str
            division : str
            season_wins : int
            season_losses : int
            winrate : double
            total_wins : int  #: all queues and seasons
            champ : str
            champ_key : str
            champ_wins : int
            champ_losses : int
            champ_winrate : double
            avg_kills : double
            avg_deaths : double
            avg_assists : double
            winrate : double
            gg_avg_kills : double
            gg_avg_deaths : double
            gg_avg_assists : double
            gg_avg_winrate : double
            deviation_kills : double
            deviation_deaths : double
            deviation_assists : double
            keystone_id : int
            spell_1 : str
            spell_2 : str
        }

    :param: summoner_name: name of one summoner in the game
    :rtype: list
    """
    blue_team = []
    red_team = []

    summoner_name = summoner_name.lower().replace(' ', '')
    summoner_id = riot.get_summoner_id(region, summoner_name)
    current_game = riot.get_current_game(region, summoner_id)
    summoner_ids = [player['summonerId'] for player in current_game['participants']]
    ranking_dict = riot.get_ranking(region, summoner_ids)

    for participant in current_game['participants']:
        champion_id = participant['championId']
        summoner_id = participant['summonerId']
        tier, division = ranking_dict[summoner_id]
        player = {
            'summoner_name': participant['summonerName'],
            'tier': tier,
            'division': division,
            'champ': riot.get_champion_name(champion_id),
            'champ_key': riot.get_champion_key(champion_id),
            'keystone_id': riot.get_keystone_id(participant['masteries']),
            'spell_1': riot.get_summoner_spell_key(participant['spell1Id']),
            'spell_2': riot.get_summoner_spell_key(participant['spell2Id'])
        }
        ranked_stats = riot.get_ranked_stats(region, participant['summonerId'])
        for champ in ranked_stats['champions']:
            if champ['id'] == 0:
                player['season_wins'] = champ['stats']['totalSessionsWon']
                player['season_losses'] = champ['stats']['totalSessionsLost']
                player['winrate'] = 0
                if player['season_wins']:
                    player['winrate'] = percentage(player['season_wins'], player['season_losses'])
                break
        for champ in ranked_stats['champions']:
            if not champ['id'] == champion_id:
                continue
            player['champ_wins'] = champ['stats']['totalSessionsWon']
            player['champ_losses'] = champ['stats']['totalSessionsLost']
            champ_games = player['champ_wins'] + player['champ_losses']
            player['avg_kills'] = round(champ['stats']['totalChampionKills'] / champ_games, 1)
            player['avg_deaths'] = round(champ['stats']['totalDeathsPerSession'] / champ_games, 1)
            player['avg_assists'] = round(champ['stats']['totalAssists'] / champ_games, 1)
            player['champ_winrate'] = 0
            if player['champ_wins']:
                player['champ_winrate'] = percentage(player['champ_wins'], player['champ_losses'])
            break
        else:
            player['champ_wins'] = 0
            player['champ_losses'] = 0
            player['avg_kills'] = 0
            player['avg_deaths'] = 0
            player['avg_assists'] = 0
            player['champ_winrate'] = 50
        avg_stats = champion_gg.get_stats()
        player['gg_avg_kills'] = avg_stats[player['champ']]['kills']
        player['gg_avg_deaths'] = avg_stats[player['champ']]['deaths']
        player['gg_avg_assists'] = avg_stats[player['champ']]['assists']
        player['gg_avg_winrate'] = avg_stats[player['champ']]['winrate']
        player['deviation_kills'] = round(player['avg_kills'] - player['gg_avg_kills'], 1)
        player['deviation_deaths'] = round(player['gg_avg_deaths'] - player['avg_deaths'], 1)
        player['deviation_assists'] = round(player['avg_assists'] - player['gg_avg_deaths'], 1)

        if participant['teamId'] == 100:
            blue_team.append(player)
        else:
            red_team.append(player)
    return blue_team, red_team


def get_recommended(summoner_name, blue_team, red_team):
    summoner_name = summoner_name.replace(" ", "").casefold()
    for player in itertools.chain(blue_team, red_team):
        if player['summoner_name'].replace(" ", "").casefold() == summoner_name:
            champion_key = player['champ_key']
            item_build = champion_gg.get_item_set(champion_key)
            starting_items = champion_gg.get_starting_items(champion_key)
            skill_order = champion_gg.get_skill_order(champion_key)

            recommended = {
                'item_build' : item_build,
                'starting_items' : starting_items,
                'skill_order' : skill_order
            }
            return recommended


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    """Render game.html with two lists (one of each team) and the recommended starting items, build path
    and skill order according to www.champion.gg.
    """
    blue_team, red_team = get_teams(region, summoner_name)
    items = get_recommended(summoner_name, blue_team, red_team)
    return render_template('game.html', region=region, summoner_name=summoner_name,
                           blue_team=blue_team, red_team=red_team, items=items)


@app.route('/random')
def random_look_up():
    return render_template('random_game.html')


if __name__ == '__main__':
    app.run(debug=True)
