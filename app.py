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
    #_users = db.users.find()
    # users_table = db.users
    db_seed()
    #profiles = db.profiles
    #NOTE: add in more dynamic features, could create game and system table, call person for USERS etc
    #first_profile = {'person': "Tom", 'top_games': "siege, gta5, idk", 'gamer_tag':"DarthGates", 'systems':"PS4, PC", 'prefered_system':"PS4"}
    #result_1 =  profiles.insert_one(first_profile)
    # first_user = {'name':"Tom",'gamer_tag':"DarthGates",'password':"test1"}
    # result_2 = users_table.insert_one(first_user)
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

    _roles = db.roles.find()
    roles = [role for role in _roles]

    _users = db.users.find()
    users = [user for user in _users]

    _systems = db.systems.find()
    systems = [system for system in _systems]

    _games = db.games.find()
    games = [game for game in _games]

    for g in games:
        print "adding system to game"
        system = db.systems.find_one({'_id': g['system_id']})
        print "Systems here", system
        g['system'] = system['short_name']

    return render_template('prlmos.html', profiles=profiles, users=users, roles=roles, systems=systems, games=games)

@app.route('/gallery', methods=['GET'])
def prlmos_gallery():
    #_profiles = db.profiles.find()
    #profiles = [profile for profile in _profiles]

    return render_template('gallery.html')#, profiles=profiles)

def db_seed():
    #Profiles of different users
    profiles = db.profiles
    profiles_array = [{'person': "Tom", 'top_games': "fallout 76", 'current_games': "red dead 2, siege, splatoon", 'gamer_tag': "DarthGates", 'systems': "PS4, PC, Switch", 'prefered_system': "PS4", 'display_color': "orange"},
             {'person': "Chris", 'top_games': "siege, fallout 76, rocket league", 'current_games': "dead by daylight, rocket league, fortnite", 'gamer_tag': "crazy_cow16", 'systems': "PS4, PC", 'prefered_system': "PS4", 'display_color': "darkorange"},
             {'person': "Tanner", 'top_games': "siege, Divinity 2, monster hunter", 'current_games': "league of legends, wow, divinity 2", 'gamer_tag': "tantanextreme2", 'systems': "PS4, PC", 'prefered_system': "PS4", 'display_color': "mediumblue"},
             {'person': "Jordan", 'top_games': "witcher 3, god of war, red dead 2", 'current_games': "red dead 2", 'gamer_tag': "Jortw91", 'systems': "PS4, Switch, PC", 'prefered_system': "PS4", 'display_color': "purple"},
             {'person': "Travis", 'top_games': "red dead 2, splatoon", 'current_games': "red dead 2, splatoon", 'gamer_tag': "darthbewbies", 'systems': "PS4, Switch", 'prefered_system': "PS4", 'display_color': "Red"},
             {'person': "Griff", 'top_games': "red dead 2", 'current_games': "red dead 2", 'gamer_tag': "so_taylor", 'systems': "PS4", 'prefered_system': "PS4", 'display_color': "Red"}]

    for p in profiles_array:
        person = profiles.find_one({'person': p['person']})
        print p['person'], person
        if person is None:
            print "Adding new user {p['person']} not found"
            result =  profiles.insert_one( p )

     #Roles of users
    roles = db.roles
    roles_array = [{'name': "Admin", 'description': "Admin role for full capabilities of web application"},
                   {'name': "User", 'description': "role for access to modify database record for a sepcific user, Users can only modify their own records"},
                   {'name': "Guest", 'description': "General access to web application, for all that arent logged in, read only access"}]

    for r in roles_array:
        role = roles.find_one({'name': r['name']})
        print r['name'], role
        if role is None:
            print "Adding new role {r['name']} not found"
            result =  roles.insert_one( r )

    #List of users
    users = db.users
    admin_role = roles.find_one({'name': "Admin"})
    user_role = roles.find_one({'name': "User"})
    users_array = [{'first_name': "Tom", 'last_initial': "M", 'role_id': admin_role['_id']},
                    {'first_name': "Chris", 'last_initial': "H", 'role_id': admin_role['_id']},
                    {'first_name': "Tanner", 'last_initial': "F", 'role_id': user_role['_id']},
                    {'first_name': "Jordan", 'last_initial': "W", 'role_id': user_role['_id']},
                    {'first_name': "Travis", 'last_initial': "M", 'role_id': user_role['_id']},
                    {'first_name': "Griff", 'last_initial': "D", 'role_id': user_role['_id']},
                    {'first_name': "Bob", 'last_initial': "M", 'role_id': user_role['_id']}]

    for u in users_array:
        user = users.find_one({'first_name': u['first_name'], 'last_initial': u['last_initial']})
        print u['first_name'], user
        if user is None:
            print "Adding new user {u['first_name']} not found"
            result =  users.insert_one( u )

    #List of systems
    systems = db.systems
    systems_array = [{'name': "Playstation 4", 'short_name': "PS4"},
                   {'name': "Xbox one", 'short_name': "Xbone"},
                   {'name': "Computer", 'short_name': "PC"},
                   {'name': "Nintendo Switch", 'short_name': "Switch"}]

    for s in systems_array:
        system = systems.find_one({'name': s['name']})
        print s['name'], system
        if system is None:
            print "Adding new system {s['name']} not found"
            result =  systems.insert_one( s )

    #List of systems
    games = db.games
    ps4 = db.systems.find_one({'short_name': "PS4"})
    switch = db.systems.find_one({'short_name': "Switch"})
    games_array = [{'name': "Tom Clancy's  Rainbow Six Siege", 'short_name': "Siege", 'system_id': ps4['_id']},
                   {'name': "Fallout 76", 'short_name': "Fallout 76", 'system_id': ps4['_id']},
                   {'name': "Red dead Redemption 2", 'short_name': "Red Dead 2", 'system_id': ps4['_id']},
                   {'name': "Splatoon", 'short_name': "Splatoon", 'system_id': switch['_id']}]

    for g in games_array:
        #Adding system to search because the same game could be on different systems
        game = games.find_one({'name': g['name'], 'system_id': g['system_id']})
        print g['name'], game
        if game is None:
            print "Adding new game {g['name']} not found"
            result =  games.insert_one( g )



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
