from flask import render_template,request,redirect
from models import LoginHandler, Decks, Record, app, db, newFlashCards, UserData
import sqlalchemy
import datetime

db.create_all()
deck_dict = dict()

for i in Decks.query.all():
	deck_dict[i.deck_name] = newFlashCards(i.deck_name)
	deck_name = deck_dict[i.deck_name]
	db.create_all()
userCred = dict()

@app.route("/", methods=["GET"])
def index():
	return render_template('login.html')

@app.route("/login", methods=["POST"])
def userLogin():
	userID = request.form["user"]
	pwd = request.form["password"]

	user = LoginHandler.query.filter_by(login_id = userID).first()
	if (pwd == user.login_pwd):
		userCred['userID'] = userID
		return redirect(f'/deck/{userID}')
	else:
		return redirect("/")

@app.route("/register", methods=["POST"])
def userRegister():
	userID = request.form["user"]
	user = LoginHandler.query.filter_by(login_id = userID).first()

	if user is None:
		pwd = request.form["pwd"]
		cpwd = request.form["cpwd"]
		if pwd == cpwd:
			newuser = LoginHandler(login_id = userID, login_pwd = pwd)
			db.session.add(newuser)
			db.session.commit()
			userCred['userID'] = userID
			return redirect(f'/deck/{userID}')
		else:
			redirect("/")

@app.route("/deck/<user_id>", methods=["GET"])
def deckManager(user_id):
	decks = Decks.query.all()
	deck_info = {i.deck_no: i.deck_name.capitalize() for i in decks}
	num_of_decks = len(deck_info)
	user_records = Record.query.filter_by(login_id = user_id)
	user_record_info = {int(i.deck_no): "Last Reviewed: "+i.last_review.strftime("%Y-%m-%d") for i in user_records}
	avg = dict()
	for num in range(1,num_of_decks+1):
		userdata = UserData.query.filter_by(user_id = user_id, deck_no = num)
		totalscore = [i.diff for i in userdata]
		if len(totalscore) > 0:
			avg[num] = sum(totalscore)/len(totalscore)
		else:
			avg[num] = 'Yet to attempt'
	return render_template('deck.html',user=user_id.capitalize(), num = len(deck_info), deck_info = deck_info, user_record_info = user_record_info, userName = user_id, avg=avg)

@app.route("/deck/<user_id>/<deck_no>/review")
def cardSelector(user_id,deck_no):
	userCred['deckno'] = deck_no
	return redirect(f'/deck/{user_id}/{deck_no}/review/1')

@app.route("/deck/<user_id>/<deck_no>/review/<card_no>")
def cardManager(user_id, deck_no, card_no):
	deck = Decks.query.filter_by(deck_no = deck_no).first()
	deckName = deck.deck_name
	cards = deck_dict[deckName].query.filter_by(sl_no = card_no).first()
	if cards is not None:
		return render_template('cards.html',deck_name = deckName.capitalize(), card_word = cards.card_word.capitalize(), card_ans = cards.card_ans.capitalize(),deck_no=deck_no,card_no=int(card_no),userName=user_id )
	else:
		Record(login_id = user_id, deck_no = deck_no, last_review = datetime.date.today())
		return redirect(f'/deck/{user_id}')

@app.route("/deck/<user_id>/add", methods=["GET","POST"])
def adddeck(user_id):
	if request.method == "POST":
		new_deck_name = request.form['deck-name']
		new_deck = deck_dict[new_deck_name] = newFlashCards(new_deck_name)
		db.create_all()
		insert_deck_name = Decks(deck_name = new_deck_name)
		db.session.add(insert_deck_name)
		db.session.commit()
		a = new_deck(card_word = request.form['first-word'], card_ans = request.form['corresponding-answer'])
		db.session.add(a)
		db.session.commit()
		return redirect(f'/deck/{user_id}')
	else:
		return render_template('adddeck.html',user_id=user_id)

@app.route('/deck/<user_id>/<deck_no>/review/<card_no>/<hardness>/next/<next_card_no>')
def difficulty(user_id, deck_no, card_no, hardness, next_card_no):
	diff_lvl = {'difficult': 3, 'medium': 2, 'easy': 1}
	UserData.query.filter_by(user_id = user_id, deck_no = deck_no, card_no = card_no).delete()
	db.session.commit()
	new_card = UserData(user_id = user_id, deck_no = deck_no, card_no = card_no, diff = diff_lvl[hardness])
	db.session.add(new_card)
	db.session.commit()
	return redirect(f'/deck/{user_id}/{deck_no}/review/{next_card_no}')

@app.route("/deck/<user_id>/<deck_no>/edit", methods=["GET","POST"])
def editdeck(user_id, deck_no):
	deck = Decks.query.filter_by(deck_no = deck_no).first()
	deckName = deck.deck_name
	cards = deck_dict[deckName].query.filter_by()
	card_info = {i.sl_no:[i.card_word.capitalize(), i.card_ans.capitalize()] for i in cards}
	return render_template("editdeck.html", num = len(card_info),user_id=user_id, deck_name=deckName.capitalize(), card_info=card_info, deck_no= deck_no)

@app.route("/deck/<user_id>/<deck_no>/delete")
def delete(user_id, deck_no):

	deckNameToBeDeleted = Decks.query.filter_by(deck_no=deck_no).first()
	deckName = deckNameToBeDeleted.deck_name
	Decks.query.filter_by(deck_no=deck_no).delete()
	db.session.commit()
	del deck_dict[deckName]

	engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
	conn = engine.connect()
	conn.execute(f'DROP TABLE {deckName}')
	db.session.commit()

	return redirect(f'/deck/{user_id}')

@app.route("/deck/<user_id>/<deck_no>/edit/<card_no>/edit", methods=["GET","POST"])
def editcard(user_id, deck_no, card_no):
	if request.method == 'POST' and request.form[confirm].lower() == 'confirm':
		deck = Decks.query.filter_by(deck_no = deck_no).first()
		deckName = deck.deck_name
		card_info = deck_dict[deckName].query.filter_by(sl_no = card_no).first()
		card_info.card_word = request.form['card-word']
		card_info.card_ans = request.form['card-ans']
		db.session.commit()
		return redirect(f'/deck/{user_id}')
	else:
		return render_template('editcard.html',user_id=user_id, deck_no=deck_no, card_no=card_no)

@app.route("/deck/<user_id>/<deck_no>/edit/<card_no>/delete", methods=["GET","POST"])
def deletecard(user_id, deck_no, card_no):
	deck = Decks.query.filter_by(deck_no = deck_no).first()
	deckName = deck.deck_name
	deck_dict[deckName].query.filter_by(sl_no = card_no).delete()
	db.session.commit()
	return redirect(f'/deck/{user_id}')

@app.route("/deck/<user_id>/<deck_no>/edit/add", methods=["GET","POST"])
def addcard(user_id, deck_no):
	if request.method == 'POST':
		deck = Decks.query.filter_by(deck_no = deck_no).first()
		deckName = deck.deck_name
		deckClass = deck_dict[deckName]
		newcard = deckClass(card_word = request.form['card-word'], card_ans = request.form['card-ans'])
		db.session.add(newcard)
		db.session.commit()
		return redirect(f'/deck/{user_id}')
	else:
		return render_template('addcard.html',user_id=user_id, deck_no=deck_no)

if __name__ == "__main__":
	app.run(
		debug=True
    )