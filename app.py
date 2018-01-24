# Application file

import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

#Set up database connection
client = MongoClient("mongodb", 27017)
#NOTE: add this as a dynamic selection of some sort so we do not need to change between modes
db = client.prlmos_dev

@app.route('/')
def home():
    _users = db.users.find()
    users_table = db.users
    profiles = db.profiles
    #NOTE: add in more dynamic features, could create game and system table, call person for USERS etc
    first_profile = {'person': "Tom", 'top_games': "siege, gta5, idk", 'gamer_tag':"DarthGates", 'systems':"PS4, PC", 'prefered_system':"PS4"}
    result_1 =  profiles.insert_one(first_profile)
    first_user = {'name':"Tom",'gamer_tag':"DarthGates",'password':"test1"}
    result_2 = users_table.insert_one(first_user)
    #users = [item for item in _items]
    #render index
    return render_template("index.html")

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
      'name': request.form['name'],
      'description': request.form['description']
    }

    #Save to DB
    db.todos.insert_one(item_doc)

    return redirect(url_for('home'))
@app.route('/prlmos_app', methods=['GET'])
def plmos_show():
    _profiles = db.profiles.find()
    profiles = [profile for profile in _profiles]

    return render_template('prlmos.html', profiles=profiles)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
