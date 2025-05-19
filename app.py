import os
from flask import Flask
from oauth import oauth
from routes.auth_routes import auth_routes
from routes.user_routes import user_routes

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialize OAuth
oauth.init_app(app)

# Register Blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)