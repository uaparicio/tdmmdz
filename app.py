import os
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)

try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error: {e}")

db = client['tdmmdzDev']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('dashboard', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/dashboard')
def dashboard():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['user_info'] = user_info
    return render_template('dashboard.html', user_info=user_info)

@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('index'))

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify({'message': 'User created', 'user_id': str(user_id)}), 201

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
    return jsonify(users), 200

# Update a user
@app.route('/users/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.json
    result = users_collection.update_one({'email': email}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User updated'}), 200

# Delete a user
@app.route('/users/<string:email>', methods=['DELETE'])
def delete_user(email):
    result = users_collection.delete_one({'email': email})
    if result.deleted_count == 0:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)