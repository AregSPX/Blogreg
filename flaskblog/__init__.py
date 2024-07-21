#we will use this to initialize our application, bringing different components. This dunder file lets know that this is a package
#making the app via a package is superior bc we solve the circular imports issue, it lets us refactor the code 


from flask import Flask       #importing the Flask class
from flask_sqlalchemy import SQLAlchemy     #SQLAlchemy - an ORM (Object Relational Mapper) - it allows us access/use different databases at once (SQLite, PostgreSQL) in an easy/object oriented way
from flask_bcrypt import Bcrypt         #a tool for hashing passwords
from flask_login import LoginManager    #a tool that handles login/logouts
from flask_mail import Mail             #a tool for sending emails
from flaskblog.config import Config



# now we're going to initialize the extensions without the app variable. All of this is done to make the further mainentance of the app easier. Thanks to this in the future we can easily test our application in under a second using unit tests, without having to check the web app manually by entering routes (pages)

db = SQLAlchemy()        #we've created a database, which is an instance of SQLAlchemy class 


bcrypt = Bcrypt()     #a tool for hashing passwords


login_manager = LoginManager()           #a tool that handles login/logouts
login_manager.login_view = 'users.login'    #flask_login - ին տեղեկացնում ենք թե որ route-ն է login-ի էջը


mail = Mail()    # a tool for sending emails






def create_app(config_class=Config):   # wrapping up the app initialization in a function so we can create different instances of it for development, testing etc. we don't include the instances here (db, login_manager, bcrypt, mail) so the app doesn't get bounded to those. for example we may not need Mail because our app doesn't send emails.
# in short it allows the reusability of this code in other places


    app = Flask(__name__)           #an instance of the class, a web application, __name__ describes the module (file) name


    with app.app_context():     # it makes the code work


        app.config.from_object(config_class)  #importing all of the configs from the specified class    (Config by default)


        # passing the initialized extenstions to the application
        db.init_app(app) 
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
        
        



        from flaskblog.users.routes import users          # importing the users blueprint, an instance of a class
        from flaskblog.posts.routes import posts          # importing the posts blueprint, an instance of a class
        from flaskblog.main.routes import main            # importing the main blueprint, an instance of a class
        from flaskblog.errors.handlers import errors      # importing the errors blueprint, an instance of a class

        app.register_blueprint(users)       # getting blueprints into play
        app.register_blueprint(posts)       # getting blueprints into play
        app.register_blueprint(main)        # getting blueprints into play
        app.register_blueprint(errors)      # getting blueprints into play


    return app      # returning the created application


