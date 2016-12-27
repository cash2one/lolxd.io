from flask import Flask, render_template
import riot


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    """Render game.html with a list of players and the recommended starting items, build path
    and skill order according to www.champion.gg.

    A player dict should look like this:
    player {
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
        summoner_spell1 : str
        summoner_spell2 : str
    }
    """
    kwargs = {}
    current_game = riot.get_current_game(region, summoner_name)
    kwargs['players'] = [player for player in current_game['participants']]
    for player in kwargs['players']:
        player['champion'] = riot.get_champion_name(player['championId'])
    return render_template('game.html', region=region, summoner_name=summoner_name, **kwargs)


@app.route('/random')
def random_look_up():
    return render_template('random_game.html')


if __name__ == '__main__':
    app.run()
