from flask import Flask, request, render_template, redirect, url_for
from catalog_utils import gen_catalog
from webcrawler import *
import json

app = Flask(__name__)
cat = gen_catalog()

@app.route("/")
def index():
	page_title = "Aggregate Pulsar Catalog"
	return render_template("index.html", page_title=page_title)

@app.route("/gen_catalog")
def initalize():
	return json.dumps(cat)

@app.route("/versioning", methods=["GET"])
def versioning():
	catalog = request.args["catalog"]
	if catalog == "ATNF":
		return get_ATNF_version()
	elif catalog == "RRATalog":
		return get_RRATalog_version()
	elif catalog == "Parallaxes":
		return get_Parallaxes_version()
	elif catalog == "GCpsr":
		return get_GCpsr_version()
	elif catalog == "frbcat":
		return get_frbcat_version()

@app.route("/render-version-box", methods=["GET"])
def render_version_box():
	is_curr = request.args["isCurrent"]
	catalog = request.args["catalog"]
	if is_curr:
		return render_template("version-box.html", image="check.png", text=catalog+" is up-to-date.")
	else:
		return render_template("version-box.html", image="red_x.png", text=catalog+" is not up-to-date.")

@app.route("/entries/<pulsar_name>")
def get_entry(pulsar_name):
	pulsar = [p for p in cat["entries"] if p["Name"] == pulsar_name][0]
	page_title = pulsar["Name"]
	return render_template("entry.html", pulsar=pulsar, page_title=page_title)

@app.route("/favicon.ico")
def favicon():
	return redirect(url_for('static', filename='favicon.ico'))