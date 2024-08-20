from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

database = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='html')
    app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)
    migrate.init_app(app, database)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User  # Import models after initializing database

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app








# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# import os
 
# database = SQLAlchemy()
# migrate = Migrate()
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# from flask_login import LoginManager

# def create_app():
#     app = Flask(__name__,template_folder='html')
#     app.config['SECRET_KEY'] =  b'_5#y2L"F4Q8z\n\xec]/'
#     app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     database.init_app(app)
    
#     login_manager = LoginManager()
#     login_manager.login_view = 'auth.login'
#     login_manager.init_app(app)

#     from .models import User

#     @login_manager.user_loader
#     def load_user(user_id):
#         # since the user_id is just the primary key of our user table, use it in the query for the user
#         return User.query.get(int(user_id))

#     # blueprint for auth routes in our app
#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     # blueprint for non-auth parts of app
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)