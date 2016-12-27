from flask import Flask, render_template
import riot


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    kwargs = {}
    current_game = riot.get_current_game(region, summoner_name)
    kwargs['players'] = [player for player in current_game['participants']]
    return render_template('game.html', region=region, summoner_name=summoner_name, **kwargs)


@app.route('/random')
def random_look_up():
    return render_template('random_game.html')


if __name__ == '__main__':
    app.run(port=5003)
