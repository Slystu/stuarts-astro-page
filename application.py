# Imports required to run the web app
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import datetime
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Users, Items
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, flash, jsonify
import requests


# Creating and binding the engine to a session
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Reading the client secrets doc
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Astro App"


# Functions to help add new users, check if a user exists
# (based on their email addess) and to get the user ID for existing users
def createUser(login_session):
    newUser = Users(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

	
# Create Google login Gconnect function (from udacity course content)
@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter. The current arg request is %s' % request.args.get('state')), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

	# Check if logged in user exists in User database. If not add 
	# them to the DB and store their user ID in the login session
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

	
# DISCONNECT - Revoke a current user's token and reset their login_session (from Udacity course content)
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user with access token %s.' % login_session['access_token'], 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON endpoint for all items
@app.route('/astro/JSON')
def astroMenuJSON():
	categories = session.query(Categories)
	items = session.query(Items)
	return jsonify(Items=[i.serialize for i in items])

# JSON endpoint to list all categories
@app.route('/astro/catJSON')
def astroCatJSON():
	categories = session.query(Categories)
	items = session.query(Items)
	return jsonify(Categories=[c.serialize for c in categories])

# JSON endpoint for all items in a specific category
@app.route('/astro/<int:category_id>/JSON')
def astroItemsforaCatJSON(category_id):
	categories = session.query(Categories).filter_by(cat_id=category_id).one()
	items = session.query(Items).filter_by(cat_id=category_id)
	return jsonify(Items=[i.serialize for i in items])

# JSON endpoint for a specific item within a specified category
@app.route('/astro/<int:category_id>/<int:item_id>/JSON')
def astroItemJSON(category_id, item_id):
	items = session.query(Items).filter_by(item_id=item_id).one()
	return jsonify(Item = items.serialize)

	
# Home page routing
@app.route('/')
@app.route('/astro')
@app.route('/astro/')
def astroCats():
	category = session.query(Categories)
	items = session.query(Items)
	if 'username' not in login_session:
		return render_template('public_catlist.html', categories=category, items=items.order_by(Items.date_added.desc()).limit(5).all())
	else:
		return render_template('catlist.html', categories=category, logged_in_user=login_session['user_id'], items=items.order_by(Items.date_added.desc()).limit(5).all())

		
# Routing to the description of an individual item within a category
@app.route('/astro/<int:category_id>/<int:item_id>')
def Description(category_id, item_id):
	category = session.query(Categories).filter_by(cat_id=category_id).one()
	selecteditem = session.query(Items).filter_by(item_id=item_id)
	itemslist = session.query(Items).filter_by(cat_id=category_id)
	creator = getUserInfo(category.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('public_description.html', categories=category, selected_item = selecteditem, items=itemslist)
	else:
		return render_template('description.html', categories=category, selected_item = selecteditem, items=itemslist)

		
# Routing to a specific category
@app.route('/astro/<int:category_id>')
def astroMenu(category_id):
	category = session.query(Categories).filter_by(cat_id=category_id).one()
	items = session.query(Items).filter_by(cat_id=category_id)
	creator = getUserInfo(category.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('public_astro.html', categories=category, items=items)
	else:
		return render_template('astro.html', categories=category, items=items)

		
# Routing for creating a new category for a logged in user
@app.route('/astro/new/', methods=['GET','POST'])
def newCat():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCat = Categories(category = request.form['category'], user_id=login_session['user_id'])
		session.commit()
		session.add(newCat)
		flash("New category created!")
		return redirect(url_for('astroCats'))
	else:
		return render_template('newcat.html')

		
# Routing for editing a category that a logged in user created
@app.route('/astro/<int:category_id>/edit', methods=['GET', 'POST'])
def editCat(category_id):
	if 'username' not in login_session:
		return redirect('/login')
	editedCat = session.query(Categories).filter_by(cat_id=category_id).one()
	if editedCat.user_id != login_session['user_id']:
		return "<script> function myfunction() {alert('You are not authorised to edit this category. Create your own category first to edit it.');}</script><body onload='myfunction()''>"
	if request.method == 'POST':
		if request.form['category']:
			editedCat.category = request.form['category']
		session.add(editedCat)
		session.commit()
		flash("Category edited!")
		return redirect(url_for('astroCats'))
	else:
		return render_template('editcat.html', category_id=category_id, categories=editedCat)

		
# Routing for a logged in user to delete one of their categories
@app.route('/astro/<int:category_id>/delete/', methods = ['GET', 'POST'])
def deleteCat(category_id):
	if 'username' not in login_session:
		return redirect('/login')
	catToDelete = session.query(Categories).filter_by(cat_id=category_id).one()
	itemsToDelete = session.query(Items).filter_by(cat_id=category_id).all()
	if catToDelete.user_id != login_session['user_id']:
		return "<script> function myfunction() {alert('You are not authorised to delete this category. Create your own category first to delete it.');}</script><body onload='myfunction()''>"
	if request.method == 'POST':
		session.delete(catToDelete)
		session.commit()
		for i in itemsToDelete:
			session.delete(i)
			session.commit()
		flash("Category and it's items deleted!")
		return redirect(url_for('astroCats'))
	else:
		return render_template('deletecat.html', category_id=category_id, categories = catToDelete)

		
# Routing for a logged in user to create an item within a category they created
@app.route('/astro/<int:category_id>/new/', methods=['GET','POST'])
def newItem(category_id):
	if 'username' not in login_session:
		return redirect('/login')
	category = session.query(Categories).filter_by(cat_id=category_id).one()
	if request.method == 'POST':
		newItem = Items(item_name = request.form['item_name'], description = request.form['description'], date_added =datetime.datetime.now(), cat_id=category_id, user_id=category.user_id)
		if newItem.user_id != login_session['user_id']:
			return "<script> function myfunction() {alert('You are not authorised to create a new item in this category. Create your own category first to add new items to it.');}</script><body onload='myfunction()''>"
		session.add(newItem)
		session.commit()
		flash("New item created!")
		return redirect(url_for('astroMenu', category_id = category_id))
	else:
		return render_template('newitem.html', cat_id=category_id)

		
# Routing for a user to edit an item they previously created
@app.route('/astro/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
	if 'username' not in login_session:
		return redirect('/login')
	editedItem = session.query(Items).filter_by(item_id=item_id).one()
	if editedItem.user_id != login_session['user_id']:
		return "<script> function myfunction() {alert('You are not authorised to edit this item. Create your own Category and Item(s) first to edit it.');}</script><body onload='myfunction()''>"
	if request.method == 'POST':
		if request.form['item_name']:
			editedItem.item_name = request.form['item_name']
			editedItem.description = request.form['description']
			editedItem.date_added = datetime.datetime.now()
		session.add(editedItem)
		session.commit()
		flash("Item edited!")
		return redirect(url_for('astroMenu', category_id = category_id))
	else:
		return render_template('edititem.html', category_id=category_id, item_id=item_id, items=editedItem)

		
# Routing for a logged in user to delete an item they previously created
@app.route('/astro/<int:category_id>/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
	if 'username' not in login_session:
		return redirect('/login')
	itemToDelete = session.query(Items).filter_by(item_id=item_id).one()
	if itemToDelete.user_id != login_session['user_id']:
		return "<script> function myfunction() {alert('You are not authorised to delete this item. Create your own Category and Item(s) first to delete it.');}</script><body onload='myfunction()''>"
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Item deleted!")
		return redirect(url_for('astroMenu', category_id = category_id))
	else:
		return render_template('deleteitem.html', category_id=category_id, item_id = item_id, item = itemToDelete)
	

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
