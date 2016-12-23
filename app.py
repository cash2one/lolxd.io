from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<region>/<summoner_name>')
def look_up(region, summoner_name):
    return 'Hello {} from {}'.format(summoner_name, region)


if __name__ == '__main__':
    app.run()
