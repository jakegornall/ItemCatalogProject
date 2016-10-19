from flask import Flask, render_template, url_for, redirect, request
import sqlite3
import time, string, datetime

def connectToDB():
    '''returns cursur object for ItemCatalog.db 
    contains the following:
    TABLE events
    date text,
    title text,
    description text'''
    conn = sqlite3.connect('ItemCatalog.db')
    return conn.cursor(), conn


app = Flask(__name__)

# makes eventsInMonth procedure callable inside templates
# app.jinja_env.globals.update(functionName=functionName)

@app.route('/')
def LandingPage():
    return render_template('landingPage.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)