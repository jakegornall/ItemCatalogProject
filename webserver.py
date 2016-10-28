from flask import Flask, render_template, url_for, redirect, request, make_response
from flask import session as login_session
import sqlite3
import time, string, datetime, random
import httplib2
from flask import jsonify
import requests
from createDB import Base, Items, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Create session and connect to DB
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# makes procedure callable inside templates
# app.jinja_env.globals.update(functionName=functionName)

BKGimages = ["/static/images/bicycle-1587515_1920.jpg",
             "/static/images/cairn-1531997_1920.jpg",
             "/static/images/venetian-1705528_1920.jpg"]

@app.route('/')
def LandingPage():
    bkg = random.choice(BKGimages)
    return render_template('landingPage.html', bkgImage=bkg)

@app.route('/newItem', methods=['POST', 'GET'])
def newItem():
    return "New Item Page"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        access_token = request.data

        # Exchange client token for long-lived server-side token.
        app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
        app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
        url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]

        # Use token to get user info from fb API.
        userinfo_url = "https://graph.facebook.com/v2.8/me"
        token = result.split("&")[0]

        url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]

        data = json.loads(result)
        login_session['state'] = state
        login_session['access_token'] = token
        login_session['provider'] = 'facebook'
        login_session['fbID'] = data['id']
        login_session['name'] = data['name']
        login_session['email'] = data['email']

        url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)

        login_session['picture'] = data['data']['url']

        userCount = session.query(Users).filter(Users.fbID == login_session['fbID']).count()
        # Add user to DB if not existing.
        if not userCount:
            newUser = Users(
                fbID=login_session['fbID'],
                name=login_session['name'],
                email=login_session['email'],
                pictureURL=login_session['picture']
                )
            session.add(newUser)
            session.commit()
            user = session.query(Users).filter(Users.fbID == login_session['fbID']).one()
            message = "Successfully added %s as new user!" % login_session['name']
            return jsonify(success=True, message=message, userID=user.id, state=login_session['state'])
        # Update user info if current user.
        if userCount:
            user = session.query(Users).filter(Users.fbID == login_session['fbID']).one()
            user.name = login_session['name']
            user.email = login_session['email']
            user.pictureURL = login_session['picture']
            session.add(user)
            session.commit()
            user = session.query(Users).filter(Users.fbID == login_session['fbID']).one()
            message = "Successfully updated %s's user info!" % login_session['name']
            return jsonify(success=True, message=message, userID=user.id, state=login_session['state'])
        else:
            message = "Error occurred while updating info."
            return jsonify(success=False, message=message)

    if request.method == 'GET':
        return render_template('login.html')

@app.route('/fbdisconnect', methods=["POST"])
def dbdisconnect():
    facebook_id = login_session['fbID']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['state']
    del login_session['access_token']
    del login_session['provider']
    del login_session['name']
    del login_session['email']
    del login_session['picture']
    del login_session['fbID']
    return "user logged"

@app.route('/<int:userID>/profile')
def profile(userID):
    if request.args.get("state") != login_session['state']:
        return redirect('/')
    else:
        bkg = random.choice(BKGimages)
        user = session.query(Users).filter(Users.id == userID).one()
        return render_template('userProfile.html', name=user.name, pictureURL=user.pictureURL, bkgImage=bkg)

@app.route('/<int:userID>/userSettings')
def UserSettings(userID):
    return "user Settings"

@app.route('/clearanceItemsAPI', methods=['GET'])
def clearanceItemsAPI():
    clearanceItems = session.query(Items).filter(Items.onClearance == 'True').all()
    return jsonify(results=[e.serialize() for e in clearanceItems])

@app.route('/saleItemsAPI', methods=['GET'])
def saleItemsAPI():
    saleItems = session.query(Items).filter(Items.onSale == 'True').all()
    return jsonify(results=[e.serialize() for e in saleItems])


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='127.0.0.1', port=5000)