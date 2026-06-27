from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET","POST"])
def login():

    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        # ✅ Secure query
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))

        result = cursor.fetchone()

        if result:
            msg = "Login Successful"
        else:
            msg = "Invalid Credentials"

    return render_template("login.html", msg=msg)

if __name__ == "__main__":
    app.run(port=5001)
