from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='.')
app.secret_key = "secret123"   # change later

# ------------------ DATABASE SETUP ------------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('index.html')

# ------------------ SIGNUP ------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                         (name, email, password))
            conn.commit()
        except:
            return "User already exists"

        return redirect('/login')

    return render_template('signup.html')

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['name']
            return redirect('/dashboard')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# ------------------ OTHER PAGES ------------------
@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/details')
def details():
    return render_template('detail.html')

# ------------------ FORGET PASSWORD ------------------
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

# ------------------
if __name__ == '__main__':
    app.run(debug=True)