from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session
)
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secure_secret_key"  # change this to something unpredictable!
CORS(app)

# MongoDB setup
client = MongoClient(
   "your_cluster_key"
)
db = client["infosetu"]
users_collection   = db.users
data_collection    = db.dashboard_data
admin_changes      = db.admin_changes

def login_required(f):
    """Simple decorator to ensure a user is logged in."""
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

# Home page
@app.route('/')
def home():
    return render_template(
        "index.html",
        name=session.get("name"),
        username=session.get("username"),
        role=session.get("role"),
        logged_in=session.get("logged_in", False)
    )

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # POST: expect JSON or form
    data = request.get_json() if request.is_json else request.form
    name     = data.get('name')
    username = data.get('username')
    password = data.get('password')
    role     = data.get('role')

    if not all([name, username, password, role]):
        return jsonify(success=False, message="All fields are required"), 400

    if users_collection.find_one({'username': username}):
        return jsonify(success=False, message="Username already exists"), 409

    hashed = generate_password_hash(password)
    users_collection.insert_one({
        'name':     name,
        'username': username,
        'password': hashed,
        'role':     role
    })

    # log them in immediately
    session['username'] = username
    session['name']     = name
    session['role']     = role
    session['logged_in'] = True

    if request.is_json:
        return jsonify(success=True,
                       redirect=url_for('dashboard')), 201
    else:
        return redirect(url_for('dashboard'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json() if request.is_json else request.form
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        # set session
        session['username']  = username
        session['name']      = user['name']
        session['role']      = user['role']
        session['logged_in'] = True

        if request.is_json:
            return jsonify(success=True,
                           redirect=url_for('dashboard')), 200
        else:
            return redirect(url_for('dashboard'))

    # invalid
    if request.is_json:
        return jsonify(success=False,
                       message="Invalid username or password"), 401
    else:
        return render_template('login.html', error="Invalid credentials"), 401

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    role     = session['role']

    if role == 'user':
        user_data = data_collection.find_one({'username': username})
        if not user_data:
            user_data = {
                'username': username,
                'search_history': [],
                'saved_pages': ['Dummy Page 1', 'Dummy Page 2'],
                'time_today': random.randint(5, 30),
                'time_month': random.randint(100, 300),
                'used_days': ["Mon", "Wed", "Fri"]
            }
            data_collection.insert_one(user_data)

        return render_template(
            'dashboard.html',
            role=role,
            name=session['name'],
            username=username,
            search_history=user_data['search_history'],
            saved_pages=user_data['saved_pages'],
            time_today=user_data['time_today'],
            time_month=user_data['time_month'],
            used_days=user_data['used_days']
        )

    elif role == 'admin':
        usage_data    = [random.randint(50, 150) for _ in range(7)]
        recent_changes = list(admin_changes
                              .find()
                              .sort('timestamp', -1))[:10]

        return render_template(
            'dashboard.html',
            role=role,
            name=session['name'],
            username=username,
            usage_data=usage_data,
            recent_changes=recent_changes
        )

    else:
        return "Invalid role", 403

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Service pages & 404
@app.route('/service/<service_name>')
@login_required
def service_page(service_name):
    allowed = ['education','healthcare','transport','agriculture','art_culture']
    if service_name not in allowed:
        return render_template('404.html'), 404
    return render_template(f"{service_name}.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
