from flask import Flask, render_template, url_for
from flask import redirect, request, make_response
from flask import session as login_session
import sqlite3
import string
import random
import httplib2
from flask import jsonify
import requests
from createDB import Base, Items, Users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import re

# Create session and connect to DB
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# makes procedure callable inside templates. Uncomment if you need to use it.
# app.jinja_env.globals.update(functionName=functionName)

BKGimages = ["/static/images/bicycle-1587515_1920.jpg",
             "/static/images/cairn-1531997_1920.jpg",
             "/static/images/venetian-1705528_1920.jpg"]


@app.route('/', methods=['GET'])
def LandingPage():
    '''Handles requests to the main landing page.'''
    bkg = random.choice(BKGimages)
    return render_template(
        'landingPage.html',
        bkgImage=bkg
        )


@app.route('/newItem', methods=['POST'])
def newItem():
    '''Handles requests to add new items to database. 
    to test functionality go to access the profile page and
    click the NEW ITEM button. This will render a modal with
    the new item form. The new item form sends a post request with
    the new item's data via ajax.'''
    if request.args.get("state") != login_session['state']:
        return jsonify(success="False", message="invalid state parameter")
    else:
        try:
            newItemObj = request.json

            name = newItemObj['name']
            price = newItemObj['price']
            description = newItemObj['description']
            imgURL = newItemObj['imgURL']
            qty = newItemObj['qty']
        except:
            return jsonify(
                success="False",
                message="Error unpacking json object.")

        if qty <= 0:
            return jsonify(
                success="False",
                message="Qty must be greater than 0.")

        if not (name, price, description, imgURL, qty):
            return jsonify(
                success="False",
                message="All fields required.")

        try:
            user = session.query(Users).filter(
                Users.fbID == login_session['fbID']).one()
            newItem = Items(
                name=name,
                sellerID=user.id,
                price=price,
                description=description,
                imageURL=imgURL,
                qty=qty)
            session.add(newItem)
            session.commit()
        except:
            return jsonify(
                success="False",
                message="Item addition unsuccessful.")

        return jsonify(success="True", message="Item Successfully Added!")


@app.route('/<int:itemID>/editItem', methods=['POST'])
def editItem(itemID):
    '''handles requests to change a particular item's data.
    Forms to edit item info is generated on the profile page.
    Item changes data is sent in a json object via ajax post request.'''
    if request.args.get("state") != login_session['state']:
        return jsonify(success="False", message="invalid state parameter")
    else:
        try:
            itemInfo = request.json

            name = itemInfo['name']
            price = itemInfo['price']
            desc = itemInfo['desc']
            imgURL = itemInfo['imgURL']
            qty = itemInfo['qty']
        except:
            return jsonify(success="False", message="Error unpacking json.")
        try:
            itemToEdit = session.query(Items).filter(Items.id == itemID).one()
        except:
            return jsonify(success="False", message="Invalid item ID")
        try:
            if int(price) < int(itemToEdit.price):
                itemToEdit.onSale = "True"
            else:
                itemToEdit.onSale = "False"

            itemToEdit.name = name
            itemToEdit.price = price
            itemToEdit.description = desc
            itemToEdit.imageURL = imgURL
            itemToEdit.qty = qty

            session.add(itemToEdit)
            session.commit()
        except:
            return jsonify(success="False", message="Could not update item.")
        return jsonify(
            success="True",
            message="Successfully updated item info!")


@app.route('/<int:itemID>/deleteItem', methods=['POST'])
def deleteItem(itemID):
    '''Handles requests to delete items from database.
    delete buttons are found on each item on the profile page.
    Request is submitted via ajax request.'''
    if request.args.get("state") != login_session['state']:
        return jsonify(success="False", message="invalid state parameter")
    else:
        try:
            item = session.query(Items).filter(Items.id == itemID).one()
        except:
            return jsonify(success="False", message="Item not in database.")

        user = session.query(Users).filter(
            Users.fbID == login_session['fbID']).one()

        if item.sellerID != user.id:
            return jsonify(
                success="False",
                message="You can only delete items that you are selling.")

        try:
            session.delete(item)
            session.commit()
        except:
            return jsonify(
                success="False",
                message="Unable to delete item at this time.")

        return jsonify(success="True", message="Item Successfully Deleted!")


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Handles login requests via facebook.'''
    if request.method == 'POST':
        state = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits) for x in xrange(32))
        access_token = request.data

        # Exchange client token for long-lived server-side token.
        app_id = json.loads(
            open('fb_client_secrets.json', 'r').read())['web']['app_id']
        app_secret = json.loads(
            open('fb_client_secrets.json', 'r').read())['web']['app_secret']
        url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # noqa
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]

        # Use token to get user info from fb API.
        userinfo_url = "https://graph.facebook.com/v2.8/me"
        token = result.split("&")[0]

        url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token  # noqa
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]

        data = json.loads(result)
        login_session['state'] = state
        login_session['access_token'] = token
        login_session['provider'] = 'facebook'
        login_session['fbID'] = data['id']
        login_session['name'] = data['name']
        login_session['email'] = data['email']

        url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token  # noqa
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)

        login_session['picture'] = data['data']['url']

        userCount = session.query(Users).filter(
            Users.fbID == login_session['fbID']).count()

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
            user = session.query(Users).filter(
                Users.fbID == login_session['fbID']).one()
            message = "Successfully added %s as new user!" % login_session['name']  # noqa
            return jsonify(
                success=True,
                message=message,
                userID=user.id,
                state=login_session['state']
                )

        # Update user info if current user.
        if userCount:
            user = session.query(Users).filter(
                Users.fbID == login_session['fbID']).one()
            user.name = login_session['name']
            user.email = login_session['email']
            user.pictureURL = login_session['picture']
            session.add(user)
            session.commit()
            user = session.query(Users).filter(
                Users.fbID == login_session['fbID']).one()
            message = "Successfully updated %s's user info!" % login_session['name']  # noqa
            return jsonify(
                success=True,
                message=message,
                userID=user.id,
                state=login_session['state']
                )
        else:
            message = "Error occurred while updating info."
            return jsonify(success=False, message=message)

    if request.method == 'GET':
        bkg = random.choice(BKGimages)
        return render_template('login.html', bkgImage=bkg)


@app.route('/fbdisconnect', methods=["POST"])
def dbdisconnect():
    '''Ends session and deletes session data upon request.
    Currently, logging out is done through the facebook logout button.
    This adds the option to implement a custom logout button if need arises.'''
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


@app.route('/<int:userID>/profile', methods=['GET'])
def profile(userID):
    '''Handles requests to the profile page.'''
    if request.args.get("state") != login_session['state']:
        return redirect('/')
    else:
        bkg = random.choice(BKGimages)
        user = session.query(Users).filter(Users.id == userID).one()
        userMerch = session.query(Items).filter(
            Items.sellerID == user.id).all()
        return render_template(
            'userProfile.html',
            name=user.name,
            pictureURL=user.pictureURL,
            bkgImage=bkg,
            userMerch=userMerch,
            state=login_session['state']
            )


@app.route('/<int:userID>/userSettings')
def UserSettings(userID):
    '''Handles requests to the user settings page.
    Not Currently implemented. Will be in future iterations of project.'''
    if request.args.get("state") != login_session['state']:
        return redirect('/')
    else:
        return "user Settings"


@app.route('/clearanceItemsAPI', methods=['GET'])
def clearanceItemsAPI():
    '''JSON endpoint for all items that are on clearance.'''
    clearanceItems = session.query(Items).filter(
        Items.onClearance == 'True').all()
    return jsonify(results=[e.serialize() for e in clearanceItems])


@app.route('/saleItemsAPI', methods=['GET'])
def saleItemsAPI():
    '''JSON endpoint for all items that are on sale.'''
    saleItems = session.query(Items).filter(Items.onSale == 'True').all()
    return jsonify(results=[e.serialize() for e in saleItems])


@app.route('/allItemsAPI', methods=['GET'])
def allItems():
    '''JSON endpoint for all items.'''
    items = session.query(Items).all()
    return jsonify(results=[e.serialize() for e in items])

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True, host='127.0.0.1', port=5000)
