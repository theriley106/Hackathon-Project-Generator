import random
from flask_sockets import Sockets
import datetime
import time
import json
import zipfile
import os
import ssl
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps as bsondumps
from pymongo import *
from datetime import datetime
from flask import *
from googleapiclient.discovery import build
import pymongo, ssl
from pymongo import MongoClient

CX = "015106168428982565841:kdznjgvin4h"
KEY = "AIzaSyAIQaiuCivVITuKtoM_myK83I8_UwwXyXc"


app = Flask(__name__, static_url_path='/static')
sockets = Sockets(app)
MESSAGES = []

PROJECTS = []

uri = 'mongodb+srv://hackhacks:Hackathons-are-super-cool!@cluster0-2o2wa.gcp.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

print("made client, making collection")
db = client.gettingStarted
people = db.people

db = client.database
hackathon_ideas = db.hackathon_ideas

# IDEAS = [x for x in open("ideas.txt").read().split("\n") if len(x) > 5 and len(x) < 200]
IDEAS = [x for x in db.hackathon_ideas.find({})]
RECENT = []
STEPS = ["Generating Project Name", "Generating Logo", "Buying Domain Name", "Raising Seed Round", "Building Starter Code", "Preparing Zip File"]
TIME_BETWEEN = 2.0
PLUS_MINUS_TIME = .5

def gen_waiting_time():
	return TIME_BETWEEN + random.uniform(PLUS_MINUS_TIME * -1, PLUS_MINUS_TIME)

@app.route("/recent", methods=["GET"])
def recent():
	info = []
	for val in RECENT:
		info.append({"title": val, "image": "https://placehold.it/150x80?text=IMAGE"})
	return jsonify({"data": info})

@app.route("/newIdea", methods=["GET"])
def get_new():
	global IDEAS
	if not IDEAS:
		IDEAS = [x for x in db.hackathon_ideas.find({})]
	index = random.randint(0, len(IDEAS)-1)
	chosenIdea = IDEAS.pop(index)
	RECENT.append(chosenIdea)
	return bsondumps(chosenIdea)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/projects', methods=['GET'])
def projects():
	sort_by = request.args.get('sort_by')
	info = get_results(page_size=8, query_str=sort_by)
	res = [{"title": x["title"], "tagline": x["tagline"], "image": x["image_url"], "oid": x["_id"], "num_likes": x["num_likes"]} for x in info]
	top3, top6 = res[:4], res[4:]
	print(top3)
	print(top6)
	return render_template("projects.html", top3=top3, top6=top6)

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
	domain = "google.com"
	projectName = "projectName"
	image = "/static/project.jpeg"
	while True:
		message = ws.receive()
		idea_id = ws.receive()
		print(idea_id)
		document = db.hackathon_ideas.find_one({"_id": ObjectId(idea_id)})
		projectName = document["title"]
		image = document["image_url"]
		base_html = gen_base_html(message)
		for i, step in enumerate(STEPS):
			html = gen_html(base_html, currentLoading=i)
			html_final = base_html + html
			ws.send(json.dumps({"html": html_final, "updated": str(datetime.now())}))
			time.sleep(gen_waiting_time())
		html = gen_html(base_html, currentLoading=1000, finish=True)

		html_2 = base_html + """<div class="row">
		<div class="col-md-6">{}</div>
		<div class="col-md-6">{}</div>
		</div><br>
		<button type="button" class="btn btn-primary btn-block" download="" onclick="location.href = '/starter?title={}&img_src={}';">Download Files</button>""".format(html, gen_final_project_html(domain, projectName, image), projectName, image)
		

		# html_2 = html_2 + ''
		ws.send(json.dumps({"html": html_2, "updated": str(datetime.now())}))
		time.sleep(.1)

@app.route('/testdata', methods=['GET'])
def test():
	personDocument = {
	"name": {"first": "Alan", "last": "Turing"},
	"birth": datetime(1912, 6, 23),
	"death": datetime(1954, 6, 7),
	"contribs": ["Turing machine", "Turing test", "Turingery"],
	"views": 1250000
	}
	return str(people.insert_one(personDocument))


@app.route('/test_image/<title>')
def test_image(title):
	return generate_image_url(title, "not using this yet")


def get_image_link(term):
	service = build("customsearch", "v1", developerKey=KEY)
	res = service.cse().list(
		q=term,
		cx=CX,
		searchType="image",
		imgType="clipart",
		num=2
	).execute()
	if "items" not in res:
		return None
	return res["items"][0]["link"]


def get_keywords(big_string):
	# pass through for now
	return big_string


def generate_image_url(title, tagline):
	default_image_link = "https://illustoon.com/photo/3813.png"
	return get_image_link(get_keywords(f'{title} {tagline}')) or default_image_link


def save_real_fake_idea(title, tagline, image_url):
	idea_document = {
		"title": title,
		"tagline": tagline,
		"image_url": image_url,
		"created_at": time.time(),
		"num_likes": 0
	}
	result = hackathon_ideas.insert_one(idea_document)
	# if success update all websockets
	# do something with result
		# probably want


@app.route('/ideas')
def get_results_endpoint():
	page_size = request.args.get('page_size')
	page_num = request.args.get('page_num')
	query_str = request.args.get('query_str')
	print(page_size)
	return bsondumps(get_results(page_size=page_size, page_num=page_num, query_str=query_str))


def get_results(page_size=50, page_num=0, query_str="created_at"):
	# handle weird stuff with strings and Nones
	page_size = 50 if page_size == None else int(page_size)
	page_num = 0 if page_num == None else int(page_num)
	query_str = "created_at" if query_str == None else query_str

	query_result = db.hackathon_ideas.find({}).sort(
		[(query_str, -1)]).skip(page_num * page_size).limit(page_size)
	return query_result


def zipdir(path, ziph, title, img_src):
	# ziph is zipfile handle
	for root, dirs, files in os.walk(path):
		for file in files:
			if file == "README.md" or file == "home.pug" or file == "header.pug":
				with open(os.path.join(root, file), mode="r") as f:
					text = f.read()
					textCopy = text
					text = text.replace("Hackathon Starter", title)
					hackathon_starter_image_url = "https://lh4.googleusercontent.com/-PVw-ZUM9vV8/UuWeH51os0I/AAAAAAAAD6M/0Ikg7viJftQ/w1286-h566-no/hackathon-starter-logo.jpg"
					text = text.replace(hackathon_starter_image_url, img_src)
					ziph.writestr(os.path.join(root, file), text)
			else:
				ziph.write(os.path.join(root, file))

@app.route('/starter', methods=['GET'])
def download_starter():
	title = request.args.get('title')
	img_src = request.args.get('img_src')
	file_name = f'{title}_starter.zip'
	zipf = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
	zipdir('./hackathon-starter-master', zipf, title, img_src)
	zipf.close()
	tmp_send = send_file(file_name, attachment_filename=file_name)
	os.remove(file_name)
	return tmp_send

@app.route('/like/<oid>', methods=['POST', 'GET'])
def like_idea(oid):
	document = db.hackathon_ideas.find_one({"_id": ObjectId(oid)})
	document["num_likes"] = document["num_likes"] + 1
	return bsondumps(db.hackathon_ideas.save(document))

if __name__ == '__main__':
	raw_input("It looks like you're trying to run this directly without web sockets.  Continue? ")
	app.run(host='127.0.0.1', port=5000)
