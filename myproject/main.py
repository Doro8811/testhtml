from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
import sqlite3

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            flash('Email already in use, please log in.')
            return redirect(url_for('login'))
        else:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            flash('Login successful!')
            return redirect(url_for('welcome', user_email=email))
        else:
            flash('Invalid email or password. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Welcome page after successful login
@app.route('/welcome/<user_email>')
def welcome(user_email):
    return f"Welcome, {user_email}!"

if __name__ == '__main__':
    app.run(debug=True)
