from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import smtplib

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
    conn.close()

init_db()

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Register User
@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                 (name, email, password))
    conn.commit()
    conn.close()

    return redirect('/')

# Login User
@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                        (email, password)).fetchone()
    conn.close()

    if user:
        return redirect('/dashboard')
    else:
        return "Invalid Login"

# SOS Alert (Email + Location)
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']

    message = f"EMERGENCY!\nUser needs help.\nLocation: https://maps.google.com/?q={lat},{lon}"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # 👇 Replace with your email & app password
        server.login("sakshinibe@gmail.com", "vzyq dine zucm tbbi")

        server.sendmail(
            "sakshinibe@gmail.com",
            "sakshinibe28@gmail.com",
            message
        )

        server.quit()
        return jsonify({"status": "Email Sent"})
    except:
        return jsonify({"status": "Error sending email"})

if __name__ == '__main__':
    app.run(debug=True)