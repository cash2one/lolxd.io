from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello world!'


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    return 'Hello {} from {}'.format(summoner_name, region)


if __name__ == '__main__':
    app.run()
