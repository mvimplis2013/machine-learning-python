import os
from flask import Flask

app = Flask(__name__) 

@app.route("/", methods=['GET', 'POST'])
def index():
	return "<h1>Hello, worl</h1>"

@app.cli.command()
def main_flask():
	click.echo("Hello, Miltos!")

