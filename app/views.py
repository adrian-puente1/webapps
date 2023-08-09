import time
import pandas as pd
import urllib.parse
import requests
import urllib.parse
import plotly.express as px
from datetime import datetime
from flask import Flask, render_template, request
from . import app

@app.route("/")
def home():
    return render_template("home.html", methods=['GET'])

@app.route("/about/")
def about():
    return render_template("about.html", methods=['GET'])

@app.route("/contact/")
def contact():
    return render_template("contact.html", methods=['GET'])

@app.route("/destination_heatmap/")
def destination_heatmap():
    if request.method=='GET':
        pass
    elif request.method=='POST':
        pass
    return render_template("destination_heatmap.html",)

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
    return render_template(
        "hello.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data", methods=['GET'])
def get_data():
    return app.send_static_file("data.json")
