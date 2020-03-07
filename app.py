from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import random

app = Flask(__name__, static_url_path='/static')

@app.route("/newIdea", methods=["GET"])
def get_new():
	ideas = [x for x in open("ideas.txt").read().split("\n") if len(x) > 5 and len(x) < 200]
	return random.choice(ideas)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)