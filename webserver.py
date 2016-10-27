from flask import Flask, render_template, url_for, redirect, request, make_response
from flask import session as login_session
import sqlite3
import time, string, datetime, random
import urllib2
from flask import jsonify
import requests
from createDB import Base, Items, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# makes procedure callable inside templates
# app.jinja_env.globals.update(functionName=functionName)

@app.route('/')
def LandingPage():
    return render_template('landingPage.html')

@app.route('/newItem', methods=['POST', 'GET'])
def newItem():
    return "New Item Page"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        responseObj = request.json
        print responseObj
        # login_session['fbID'] = responseObj.me.userID
        # login_session['name'] = responseObj.me.name
        # login_session['access_token'] = responseObj.fbResponse.accessToken
        # login_session['state'] = state
        # user = session.query(Users).filter(Users.fbID == login_session['fbID']).one()
        # if not user:
        #     newUser = Users(fbID=login_session['fbID'], name=login_session['name'])
        #     session.add(newUser)
        return "Success!"
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/<int:userID>/profile')
def profile(userID):
    user = session.query(Users).filter(Users.id == userID).one()
    return render_template('userProfile.html', user=user)

@app.route('/<int:userID>/userSettings')
def UserSettings(userID):
    return "user Settings"

@app.route('/<int:userID>/logout')
def Logout(userID):
    return "logout"

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