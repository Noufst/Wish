# Imports from flask
from flask import Flask, render_template, jsonify
from flask import request, flash, redirect, url_for

# to be able to store datetime to the database
import datetime

# imports for Google OAuth
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import requests
import random
import string
import httplib2
import json

# imports for the database
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Flask instance
app = Flask(__name__)

# Connect to the database and create database session
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Google OAuth client id
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog"


@app.route('/')
def showHomePage():
    categories = session.query(Category).all()
    latestItems = session.query(Item).order_by(desc(Item.dateAdded)).limit(3).all()
    return render_template('index.html', categories=categories, latestItems=latestItems)


@app.route('/catalog/add', methods=['GET','POST'])
def addItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        user = getUserInfo(login_session['user_id'])
        category = session.query(Category).filter_by(id = request.form['categories']).one()
        newItem = Item(name = request.form['name'], description = request.form['description'], dateAdded = datetime.datetime.now().isoformat(), category = category, user = user)
        session.add(newItem)
        session.commit()
        flash("New Item Added Successfully!")
        return redirect(url_for("showCatalogItems", category_name = category.name))
    else:
        categories = session.query(Category).all()
        return render_template('addItem.html', categories = categories)


@app.route('/catalog/<string:category_name>/items')
def showCatalogItems(category_name):
    category = session.query(Category).filter_by(name = category_name).first()
    items = session.query(Item).filter_by(category_id = category.id)
    return render_template('category.html', category = category, items = items)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItemDetails(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).first()
    item = session.query(Item).filter_by(name = item_name).first()
    owner = getUserInfo(item.user_id)
    if 'username' not in login_session or owner.id != login_session['user_id']:
        return render_template('item.html', category = category, item = item, isOwner = False)
    else:
        return render_template('item.html', category = category, item = item, isOwner = True)


@app.route('/catalog/<string:item_name>/edit', methods=['GET','POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    item = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['categories']:
            category = session.query(Category).filter_by(id = request.form['categories']).one()
            item.category = category
            item.category_id = request.form['categories']
        session.commit()
        flash('Item Edited Successfully')
        return redirect(url_for("showHomePage"))
    else:
        categories = session.query(Category).all()
        return render_template('editItem.html', item= item, categories = categories)

@app.route('/catalog/<string:item_name>/delete', methods=['GET','POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    item = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Deleted Successfully')
        return redirect(url_for("showHomePage"))
    else:
        return render_template('deleteItem.html', item = item)


@app.route('/catalog/json')
def showCatalogJson():
    categories_dict = []
    categories = session.query(Category).all()
    for category in categories:
        items_dict = []
        items = session.query(Item).filter_by(category_id = category.id).all()
        for item in items:
            item_dict = item.serialize
            items_dict.append(item_dict)
        category_dict = {
        'id': category.id,
        'name': category.name,
        'items': items_dict
        }
        categories_dict.append(category_dict)
    return jsonify(Category = categories_dict)

# Login routes
@app.route('/login')
def showLogin():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
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

    # Check if user exist. if it doesn't, make a new user
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


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        return redirect(url_for('showHomePage'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
