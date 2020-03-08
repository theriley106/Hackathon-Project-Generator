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

STEPS = ["Generating Project Name", "Generating Logo", "Buying Domain Name", "Raising Seed Round", "Building Starter Code", "Preparing Zip File"]
TIME_BETWEEN = 0
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
	baseHTML = ""
	for i, step in enumerate(STEPS):
		if step == "Buying Domain Name" and currentLoading > STEPS.index("Buying Domain Name"):
			baseHTML += """<h5><img height="24px" width="24px" src="/static/check.png"></img>{} (not really xD)</h5>""".format(step)
		elif i == currentLoading:
			baseHTML += """<h5><img height="24px" width="24px" src="/static/load.gif"></img>{}</h5>""".format(step)
		elif currentLoading > i:
			baseHTML += """<h5><img height="24px" width="24px" src="/static/check.png"></img>{}</h5>""".format(step)
		else:
			baseHTML += """<h5 style='padding-left:24px; padding-bottom:4px;'>{}</h5>""".format(step)
	return baseHTML

def gen_final_project_html(domain, projectName, image):
	return """
		  <img height="125px" width="225px" src="{}">
		  <img src="/static/winner.png" class="imtip">
		<p style="text-align: left;padding-top:5px;">Name: <font color="blue"><b>{}</b></font></p>
		<p style="text-align: left;">Domain: <font color="blue"><b>{}</b></font></p>""".format(image, projectName, domain)
		
		

@sockets.route('/echo')
def echo_socket(ws):
	while True:
		message = ws.receive()
		base_html = gen_base_html(message)
		for i, step in enumerate(STEPS):
			html = gen_html(base_html, currentLoading=i)
			html_final = base_html + html
			ws.send(json.dumps({"html": html_final, "updated": str(datetime.datetime.now())}))
			time.sleep(gen_waiting_time())
		html = gen_html(base_html, currentLoading=1000, finish=True)

		domain = "google.com"
		projectName = "projectName"
		image = "/static/project.jpeg"

		html_2 = base_html + """<div class="row">
		<div class="col-md-6">{}</div>
		<div class="col-md-6">{}</div>
		</div><br>
		<button type="button" class="btn btn-primary btn-block">Download Files</button>""".format(html, gen_final_project_html(domain, projectName, image))
		

		# html_2 = html_2 + ''
		ws.send(json.dumps({"html": html_2, "updated": str(datetime.datetime.now())}))
		time.sleep(.1)

if __name__ == '__main__':
	raw_input("It looks like you're trying to run this directly without web sockets.  Continue? ")
	app.run(host='127.0.0.1', port=5000)