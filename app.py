from flask import Flask, render_template
import riot
import champion_gg


app = Flask(__name__)


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
    ranking_dict = riot.get_ranking(region, [player['summonerId'] for player in current_game['participants']])
    for player in current_game['participants']:
        champion_id = player['championId']
        summoner_id = player['summonerId']
        tier, division = ranking_dict[summoner_id]
        player_dict = {
            'summoner_name': player['summonerName'],
            'tier': tier,
            'division': division,
            'champ': riot.get_champion_name(champion_id),
            'champ_key': riot.get_champion_key(champion_id),
            'keystone_id': riot.get_keystone_id(player['masteries']),
            'spell_1': riot.get_summoner_spell_key(player['spell1Id']),
            'spell_2': riot.get_summoner_spell_key(player['spell2Id'])
        }
        ranked_stats = riot.get_ranked_stats(region, player['summonerId'])
        for champ in ranked_stats['champions']:
            if champ['id'] == 0:
                player_dict['season_wins'] = champ['stats']['totalSessionsWon']
                player_dict['season_losses'] = champ['stats']['totalSessionsLost']
                player_dict['winrate'] = 0
                if player_dict['season_wins']:
                    player_dict['winrate'] = round(player_dict['season_wins'] / (player_dict['season_wins'] + player_dict['season_losses']), 1)
                break
        for champ in ranked_stats['champions']:
            if not champ['id'] == champion_id:
                continue
            player_dict['champ_wins'] = champ['stats']['totalSessionsWon']
            player_dict['champ_losses'] = champ['stats']['totalSessionsLost']
            champ_games = player_dict['champ_wins'] + player_dict['champ_losses']
            player_dict['avg_kills'] = round(champ['stats']['totalChampionKills'] / champ_games, 1)
            player_dict['avg_deaths'] = round(champ['stats']['totalDeathsPerSession'] / champ_games, 1)
            player_dict['avg_assists'] = round(champ['stats']['totalAssists'] / champ_games, 1)
            player_dict['champ_winrate'] = 100
            if player_dict['champ_wins']:
                player_dict['champ_winrate'] = round(player_dict['champ_wins'] / (player_dict['champ_wins'] + player_dict['champ_losses']), 1)
            break
        else:
            player_dict['champ_wins'] = 0
            player_dict['champ_losses'] = 0
            player_dict['avg_kills'] = 0
            player_dict['avg_deaths'] = 0
            player_dict['avg_assists'] = 0
            player_dict['winrate'] = 50
        avg_stats = champion_gg.get_stats()
        player_dict['gg_avg_kills'] = avg_stats[player_dict['champ']]['kills']
        player_dict['gg_avg_deaths'] = avg_stats[player_dict['champ']]['deaths']
        player_dict['gg_avg_assists'] = avg_stats[player_dict['champ']]['assists']
        player_dict['gg_avg_winrate'] = avg_stats[player_dict['champ']]['winrate']
        player_dict['deviation_kills'] = round(player_dict['avg_kills'] - player_dict['gg_avg_kills'], 1)
        player_dict['deviation_deaths'] = round(player_dict['avg_deaths'] - player_dict['gg_avg_deaths'], 1)
        player_dict['deviation_assists'] = round(player_dict['avg_assists'] - player_dict['gg_avg_deaths'], 1)

        if player['teamId'] == 100:
            blue_team.append(player_dict)
        else:
            red_team.append(player_dict)
    return blue_team, red_team


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    """Render game.html with two lists (one of each team) and the recommended starting items, build path
    and skill order according to www.champion.gg.
    """
    blue_team, red_team = get_teams(region, summoner_name)
    return render_template('game.html', region=region, summoner_name=summoner_name,
                           blue_team=blue_team, red_team=red_team)


@app.route('/random')
def random_look_up():
    return render_template('random_game.html')


if __name__ == '__main__':
    app.run(debug=True)
