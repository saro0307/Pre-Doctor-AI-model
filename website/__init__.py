from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

DB_NAME = "database.db"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abc123"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    from .views import views
    from .upgrade import upgrade
    # from .auth import auth
    # from .dummy import dummy
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(upgrade, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(dummy, url_prefix='/')
    from .models import History
    with app.app_context():
        db.create_all()
        print("Database created!")
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app=app)
    # login_manager.remember_cookie_duration = timedelta(days=1)
    #
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))
    return app
