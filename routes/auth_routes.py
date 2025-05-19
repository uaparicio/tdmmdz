from flask import Blueprint, render_template, redirect, url_for, session
from oauth import google

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def index():
    return render_template('index.html')

@auth_routes.route('/login')
def login():
    redirect_uri = url_for('auth.dashboard', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_routes.route('/dashboard')
def dashboard():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['user_info'] = user_info
    return render_template('dashboard.html', user_info=user_info)

@auth_routes.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('auth.index'))