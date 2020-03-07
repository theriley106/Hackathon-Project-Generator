from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import random
from flask_sockets import Sockets
import datetime
import time
import json


app = Flask(__name__, static_url_path='/static')
sockets = Sockets(app)
MESSAGES = []

PROJECTS = []

STEPS = ["Generating Project Name", "Generating Logo", "Generating Domain Name", "Raising Seed Round", "Building Starter Code", "Preparing Zip File"]
TIME_BETWEEN = 2.0
PLUS_MINUS_TIME = .5

def gen_waiting_time():
	return TIME_BETWEEN + random.uniform(PLUS_MINUS_TIME * -1, PLUS_MINUS_TIME)

@app.route("/newIdea", methods=["GET"])
def get_new():
	ideas = [x for x in open("ideas.txt").read().split("\n") if len(x) > 5 and len(x) < 200]
	return random.choice(ideas)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

def gen_base_html(message):
	html = """<center><h4><br><b>{}</b></h4><br></center>""".format(message)
	return html

def gen_html(baseHTML, currentLoading=0, finish=False):
	for i, step in enumerate(STEPS):
		if i == currentLoading:
			baseHTML += """<h5><img height="24px" width="24px" src="/static/load.gif"></img>{}</h5>""".format(step)
		elif currentLoading > i:
			baseHTML += """<h5><img height="24px" width="24px" src="/static/check.png"></img>{}</h5>""".format(step)
		else:
			baseHTML += """<h5 style='padding-left:24px;'>{}</h5>""".format(step)
	if finish:
		baseHTML += """<br><button type="button" class="btn btn-primary btn-block">Download Files</button>"""
	return baseHTML
		

@sockets.route('/echo')
def echo_socket(ws):
    while True:
    	message = ws.receive()
    	base_html = gen_base_html(message)
    	for i, step in enumerate(STEPS):
    		html = gen_html(base_html, currentLoading=i)
    		ws.send(json.dumps({"html": html, "updated": str(datetime.datetime.now())}))
    		time.sleep(gen_waiting_time())
    	html = gen_html(base_html, currentLoading=1000, finish=True)
    	ws.send(json.dumps({"html": html, "updated": str(datetime.datetime.now())}))
        time.sleep(.1)

if __name__ == '__main__':
	raw_input("It looks like you're trying to run this directly without web sockets.  Continue? ")
	app.run(host='127.0.0.1', port=5000)