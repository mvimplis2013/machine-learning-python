import click
from flask import Flask

app = Flask(__name__) 

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
	
@app.cli.command()
def main_flask():
	click.echo("Hello, Miltos!")

