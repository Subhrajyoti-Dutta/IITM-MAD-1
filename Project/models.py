from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import sqlalchemy

#create a Flask Instance
app=Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
#Initialize the database
db=SQLAlchemy(app)

class LoginHandler(db.Model):
	__tablename__ = 'login'
	login_id = db.Column(db.String, primary_key=True, unique = True)
	login_pwd = db.Column(db.String)

class Decks(db.Model):
	__tablename__ = 'deck'
	deck_no = db.Column(db.Integer, primary_key=True,autoincrement=True)
	deck_name = db.Column(db.String, unique = True)

class Record(db.Model):
	__tablename__ = 'record'
	login_id = db.Column(db.String, db.ForeignKey('login.login_id'), primary_key=True)
	deck_no = db.Column(db.String, db.ForeignKey('deck.deck_no'), primary_key=True)
	last_review = db.Column(db.Date)

class UserData(db.Model):
	__tablename__ = 'userdata'
	user_id = db.Column(db.String, primary_key=True)
	deck_no = db.Column(db.String, db.ForeignKey('deck.deck_no'), primary_key=True)
	card_no = db.Column(db.Integer, primary_key=True)
	diff = db.Column(db.Integer)

def newFlashCards(deckName):
	class FlashCardsMaker(db.Model):
		__tablename__ = deckName
		sl_no = db.Column(db.Integer,primary_key=True,autoincrement=True)
		card_word = db.Column(db.String)
		card_ans = db.Column(db.String)
	return FlashCardsMaker

if __name__ == "__main__":
	db.create_all()