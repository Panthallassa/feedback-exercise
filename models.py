from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), 
                         primary_key=True,
                         unique=True,
                         nullable=False)
    
    password = db.Column(db.Text, 
                         nullable=False)
    
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                           nullable=False)
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user with hashed password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate the user exsists and password is correct"""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    

class Feedback(db.Model):
    """Feedback model"""

    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,
                   nullable=False,
                   autoincrement=True)
    
    title = db.Column(db.String(100),
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False)
    
    user = db.relationship('User', backref='feedback')
    

