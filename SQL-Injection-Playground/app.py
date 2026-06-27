from flask import Flask, request, render_template
import sqlite3
from detector import detect_sqli

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET","POST"])
def login():

    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Detect SQLi
        if detect_sqli(username) or detect_sqli(password):
            with open("logs.txt","a") as f:
                f.write(f"SQLi attempt: {username} | {password}\n")

        conn = get_db()
        cursor = conn.cursor()

        # ❌ Vulnerable query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                msg = "Login Successful"
            else:
                msg = "Invalid Credentials"

        except:
            msg = "SQL Error"

    return render_template("login.html", msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
