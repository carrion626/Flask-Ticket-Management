from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = "PLEASE LOG IN TO PROCEED"
login.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object('data.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import authentication, ticket, users
    app.register_blueprint(authentication.auth_bp)
    app.register_blueprint(ticket.ticket_bp)
    app.register_blueprint(users.user_bp)

    return app
