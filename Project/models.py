from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

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
	record_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
	login_id = db.Column(db.String, db.ForeignKey('login.login_id'))
	deck_no = db.Column(db.String, db.ForeignKey('deck.deck_no'))
	last_review = db.Column(db.Date)

def newFlashCards(deckName):
	class FlashCardsMaker(db.Model):
		__tablename__ = deckName
		sl_no = db.Column(db.Integer,primary_key=True,autoincrement=True)
		card_word = db.Column(db.String)
		card_ans = db.Column(db.String)
	return FlashCardsMaker

db.create_all()
if __name__ == "__main__":
	a = Record(login_id = 'root', deck_no = '1', last_review = datetime.date.today())
	db.session.add(a)
	db.session.commit()