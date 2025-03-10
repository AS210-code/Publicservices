import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Connection
app.config["MONGO_URI"] = "mongodb+srv://ankitasahariamld:NnX60wksmH6mJAcd@cluster0.zzexl.mongodb.net/public_services_db?retryWrites=true&w=majority"
mongo = PyMongo(app)

try:
    mongo.db.command('ping')
    print("✅ Successfully connected to MongoDB: public_services_db!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

backend_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
frontend_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(backend_templates),
    FileSystemLoader(frontend_templates)
])

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_id, username, password, role):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user["_id"]), user["username"], user["password"], user["role"])
    return None

# Serve Frontend Pages Correctly
@app.route('/')
@login_required
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            user_obj = User(str(user['_id']), user['username'], user['password'], user['role'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        return 'Invalid Credentials'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form.get('role', 'user')
        new_user = {"username": username, "password": password, "role": role}
        mongo.db.users.insert_one(new_user)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/state/<state_name>')
def state_page(state_name):
    return render_template(f'states/{state_name}.html')

# API Endpoints for Services
@app.route('/api/services', methods=['GET'])
def get_services():
    services = mongo.db.services.find()
    result = [{"_id": str(service['_id']), **service} for service in services]
    return jsonify(result)

@app.route('/api/apply', methods=['POST'])
@login_required
def apply_service():
    data = request.json
    data['user_id'] = current_user.id
    result = mongo.db.applications.insert_one(data)
    return jsonify({"message": "Application submitted", "id": str(result.inserted_id)})

@app.route('/api/admin/services', methods=['POST'])
@login_required
def add_service():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    result = mongo.db.services.insert_one(data)
    return jsonify({"message": "Service added", "id": str(result.inserted_id)})

@app.route('/api/admin/services/<service_id>', methods=['PUT'])
@login_required
def update_service(service_id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    mongo.db.services.update_one({"_id": ObjectId(service_id)}, {"$set": data})
    return jsonify({"message": "Service updated"})

@app.route('/api/admin/services/<service_id>', methods=['DELETE'])
@login_required
def delete_service(service_id):
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    mongo.db.services.delete_one({"_id": ObjectId(service_id)})
    return jsonify({"message": "Service deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

