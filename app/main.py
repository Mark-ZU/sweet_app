from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Guest, Table
from .storedmodels import Chart
import json

main = Blueprint('main',__name__)

chart = None
@main.route('/')
def index():
    return render_template("index.html")

@main.route('/profile')
@login_required
def profile():
    global chart
    if chart == None:
        chart = Chart()
    return render_template("profile.html", data={
        "tables":chart.tables,
        "guests":chart.guests,
        "seats_pos":chart.pos_seat
    })

@main.route('/send/', methods=['GET','POST'])
def send():
    if request.method != "POST":
        return jsonify(status='OK')
    data = json.loads(request.form['data'])
    global chart
    res,msg,changed = chart.deal(data['type'],data['data'])
    return jsonify(status=res,msg=msg,changed=changed,data={
        "tables":chart.tables,
        "guests":chart.guests,
    })