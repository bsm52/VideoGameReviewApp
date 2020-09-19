import sqlite3
import flask
import os
import datetime
from flask import jsonify, request, render_template, session
from passlib.hash import sha256_crypt

app = flask.Flask(__name__)
app.config["DEBUG"] = True

app.secret_key = f"{os.urandom(15)}"


@app.route('/', methods=["POST", "GET"])
def form():

    if request.method == "POST":

        name = request.form["gamename"]

        console = request.form["console"]

        conn = sqlite3.connect(r"C:\Users\Brandon\Desktop\test.db")

        cur = conn.cursor()

        sql = "insert into games(console, name) values (?, ?)"

        cur.execute(sql, (console,name))

        conn.commit()


    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    if session.get('loggedon'):
        if session['loggedon'] == True:

            return(f"you are already logged in as {session['user']}"), 200

    elif request.method == "POST" :
        username = request.form['username']

        password = request.form['password']

        conn = sqlite3.connect(r"C:\Users\Brandon\Desktop\test.db")

        cursor = conn.cursor()

        sql = "select password from users where username = ?"

        cursor.execute(sql, (username,))

        resultingPw = cursor.fetchone()

        ifMatch = sha256_crypt.verify(password, resultingPw[0])

        if ifMatch:

            sql = "update Users set lastloggedindate = ? where username = ?"

            cursor.execute(sql, (datetime.datetime.now(),username))

            conn.commit()

            session['user'] = username

            session['loggedon'] = True
    
    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():

    session['loggedon'] = False

    session['user'] = ""

    return render_template("login.html")

    


@app.route('/createuser', methods=["GET", "POST"])
def createuser():

    if request.method == "POST":

        username = request.form['username']

        password = request.form['password']

        name = request.form['name']

        hashedpw = sha256_crypt.hash(password)

        conn = sqlite3.connect(r"C:\Users\Brandon\Desktop\test.db")

        cursor = conn.cursor()

        sql = "insert into Users(name, username, password) values (?,?,?)"

        cursor.execute(sql, (name, username, hashedpw))

        conn.commit()


    return render_template("CreateUser.html")




@app.route('/api', methods=["GET", "POST"])
def getGames():

    conn = sqlite3.connect(r"C:\Users\Brandon\Desktop\test.db")

    cur = conn.cursor()

    if request.method == 'GET':

        console = request.args['console']

        sql = "select * from games where console = ?"

        cur.execute(sql, (console,))

        results = cur.fetchall()

        return jsonify(results)

    elif request.method == 'POST':

        console = request.args['console']

        name = request.args['name']

        sql = "insert into games(console, name) values (?, ?)"

        cur.execute(sql, (console,name))

        conn.commit()

        return 'All good!', 200



@app.route('/save', methods=['POST'])
def saveGame():

    console = request.args['console']
    name = request.args['name']

    dict = {
        'name' : name,
        'console' : console
    }

    return jsonify(dict)


@app.route('/saveJSON', methods=['POST'])
def saveJSON():
    data = request.get_json()
    console = data['console']
    name = data['name']

    dict = {
        'name' : name,
        'console' : console
    }

    return jsonify(dict)

app.run()
