# Application file
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION

app = Flask(__name__)
Bootstrap(app)

#Set up database connection
client = MongoClient("mongodb", 27017)
#NOTE: add this as a dynamic selection of some sort so we do not need to change between modes
db = client.prlmos_dev

nav = Nav()


@nav.navigation()
def mainNavBar():
    return Navbar(
      'prlmos',
      View('Home', 'home'),
      View('The Team', 'prlmos_show'),
      View('Gallery', 'prlmos_gallery'),
    #   Subgroup(
    #     'Docs',
    #     Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
    #     Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
    #     Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
    #     Separator(),
    #     Text('Bootstrap'),
    #     Link('Getting started', 'http://getbootstrap.com/getting-started/'),
    #     Link('CSS', 'http://getbootstrap.com/css/'),
    #     Link('Components', 'http://getbootstrap.com/components/'),
    #     Link('Javascript', 'http://getbootstrap.com/javascript/'),
    #     Link('Customize', 'http://getbootstrap.com/customize/'), ),
    # Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)),
    )

nav.init_app(app)

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

@app.route('/new_user', methods=['POST'])
def new_user():
    item_doc = {
      'name': request.form['name'],
      'description': request.form['description']
    }



    #Save to DB
    #db.todos.insert_one(item_doc)

    return redirect(url_for('home'))

@app.route('/prlmos', methods=['GET'])
def prlmos_show():
    _profiles = db.profiles.find()
    profiles = [profile for profile in _profiles]

    return render_template('prlmos.html', profiles=profiles)

@app.route('/gallery', methods=['GET'])
def prlmos_gallery():
    #_profiles = db.profiles.find()
    #profiles = [profile for profile in _profiles]

    return render_template('gallery.html')#, profiles=profiles)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
