####whoop best blog evar
from flask import Flask, render_template, request, redirect, g, url_for, flash
import sqlite3
import csv
import os.path
import numpy

app = Flask(__name__) #Create flask object
app.config.from_object(__name__) #add configuration information

if not os.path.isfile("softBlog.db"):
    conn = sqlite3.connect("softBlog.db")

    curs = conn.curosr()
    q = """CREATE TABLE posts(title text, post text, time real, pId integer)
    CREATE TABLE comments(comment text, time real, pId integer, cID integer)"""

    curs.execute(q)
    conn.commit()

@app.route("/")
def index():



#Configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'dontputthisongithub' #hurr
USERNAME = 'admin'
PASSWORD = 'notongithub'

if __name__ == "__main__":
    app.debug=True
    app.run()



def addPost (title, post, time, pID):
    conn = sqlite3.connect("softBlog.db")

    curs = conn.curosr()

    #Sorry I am unsure about the string substitutions so could someone else tackle that
    BASE = "insert into posts values(" + title + "," + post + "," + time + "," + pID + ")"

    res = BASE

    curs.execute(res)

    conn.commit()


def addComment (comment, time, pID, cID):
    conn = sqlite3.connect("softBlog.db")

    curs = conn.curosr()

    #Sorry I am unsure about the string substitutions so could someone else tackle that
    BASE = "insert into comments values(" + post + "," + time + "," + pID + "," + cID + ")"

    res = BASE

    curs.execute(res)

    conn.comment()

def trending(a):
    one = 0
    oneCount = 0
    two = 0
    twoCount = 0
    three = 0
    threeCount = 0
    for post in a:
        count = 0
        for time in post:
            if time - time.time() <= 86400:
                count += 1
        if count > oneCount:
            three = two
            threeCount = twoCount
            two = one
            twoCount = oneCount 
            one = post[0]
            oneCount = count
        elif count >= twoCount:
            three = two
            threeCount = twoCount
            two = post[0]
            twoCount = count
        elif count >= threeCount:
            three = post[0]
            threeCount = count
    return [one,two,three]

    

    
