from flask import Flask, render_template
import riot
import champion_gg


app = Flask(__name__)


def get_teams(region, summoner_name):
    """Return two lists representing the players on blue and red team respectively.

    A player dictionary looks like this:
        player {
            summoner_name : str
            season_wins : int
            season_losses : int
            total_wins : int  #: all queues and seasons
            champ : str
            champ_wins : int
            champ_losses : int
            avg_kills : double
            avg_deaths : double
            avg_assists : double
            gg_avg_kills : double
            gg_avg_deaths : double
            gg_avg_assists : double
            spell_1 : str
            spell_2 : str
        }

    :param summoner_name: name of one summoner in the game
    :rtype: list
    """
    blue_team = []
    red_team = []
    summoner_name = summoner_name.lower().replace(' ', '')
    summoner_id = riot.get_summoner_id(region, summoner_name)
    current_game = riot.get_current_game(region, summoner_id)
    for player in current_game['participants']:
        champion_id = player['championId']
        player_dict = {
            'summoner_name': player['summonerName'],
            'champ': riot.get_champion_name(champion_id),
            'spell_1': riot.get_summoner_spell_name(player['spell1Id']),
            'spell_2': riot.get_summoner_spell_name(player['spell2Id'])
        }
        ranked_stats = riot.get_ranked_stats(region, player['summonerId'])
        for champ in ranked_stats['champions']:
            if champ['id'] == 0:
                player_dict['season_wins'] = champ['stats']['totalSessionsWon']
                player_dict['season_losses'] = champ['stats']['totalSessionsLost']
                break
        for champ in ranked_stats['champions']:
            if not champ['id'] == champion_id:
                continue
            player_dict['champ_wins'] = champ['stats']['totalSessionsWon']
            player_dict['champ_losses'] = champ['stats']['totalSessionsLost']
            player_dict['avg_kills'] = champ['stats']['totalChampionKills']
            player_dict['avg_deaths'] = champ['stats']['totalDeathsPerSession']
            player_dict['avg_assists'] = champ['stats']['totalAssists']
            break
        avg_stats = champion_gg.get_stats()
        player_dict['gg_avg_kills'] = avg_stats[player_dict['champ']]['kills']
        player_dict['gg_avg_deaths'] = avg_stats[player_dict['champ']]['deaths']
        player_dict['gg_avg_assists'] = avg_stats[player_dict['champ']]['assists']


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
    app.run()
