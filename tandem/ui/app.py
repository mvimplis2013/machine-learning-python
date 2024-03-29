import click
from flask import Flask, render_template

app = Flask(__name__) 

user = {
	'username': 'Grey Li',
	'bio': 'From Other Country'
}

movies = [
	{'name': 'My Neighbor Totoro', 'year': '1988'},
	{'name': 'Three Colours Trilogy', 'year': '1993'},
]

@app.route("/watchlist")
def watchlist():
	return render_template("watchlist.html", user=user, movies=movies)

@app.route("/watchlist2")
def watchlist_with_static():
	return render_template('watchlist_with_static.html', user=user, movies=movies) 

@app.route("/", methods=['GET', 'POST'])
def index():
	return "<h1>Hello, world !</h1>"

@app.route("/hi")
@app.route("/hello")
def say_hello():
	return "<h1>Hello, flask !</h1>"

# Dynamic Route
@app.route("/greet", defaults={"name": "Pete"})
def greet(name):
	return "<h1>Hello, %s !</h1>" %name 

# Video.js - HTML5 Video Player
@app.route("/load-media")
def load_media():
	return render_template("load-media.html")
	
@app.cli.command()
def main_flask():
	click.echo("Hello, Miltos!")

