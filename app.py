import os
from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

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

if __name__ == '__main__':
    app.run(debug=True)