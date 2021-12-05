from .database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model,UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    firstname = db.Column(db.String,nullable=False)
    lastname =  db.Column(db.String,nullable=True)
    user_name = db.Column(db.String,nullable=False,unique=True)
    hashed_password = db.Column(db.String, nullable=False)
    # Creating One-to-Many Relationship
    decks=db.relationship("Deck",backref='owner')

    @property
    def password(self):
        raise AttributeError("Password ain't a readable attribute!")
    
    @password.setter
    def password(self,password):
        self.hashed_password = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return (self.user_id)
    
    def __repr__(self):
        return '<Name %r>' % self.user_name

# Deck Model 
class Deck(db.Model):
    __tablename__ = "deck"
    deck_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    deck_name = db.Column(db.String,nullable=False)
    owner_userid=db.Column(db.Integer,db.ForeignKey("user.user_id"))
    last_reviewed = db.Column(db.Integer)
    deck_score = db.Column(db.Integer)
    # creating One-to-Many Relationship
    cards=db.relationship("Card",backref='Deck')

    def __repr__(self):
        return '<Name %r>' % self.deck_name

# Card Model
class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deck_id = db.Column(db.Integer,db.ForeignKey("deck.deck_id"))
    question = db.Column(db.String,nullable=False)
    answer = db.Column(db.String,nullable=False)
    card_score = db.Column(db.Integer)
    last_reviewed = db.Column(db.Integer)
