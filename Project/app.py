from flask import render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from models import LoginHandler, Decks, Record, app, db

@app.route("/", methods=["GET","POST"])
def index():
	return render_template('login.html')


@app.route("/login", methods=["POST"])
def userLogin():
	userID = request.form["user"]
	pwd = request.form["password"]

	user = LoginHandler.query.filter_by(login_id = userID).first()
	if (pwd == user.login_pwd):
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
			return redirect(f'/deck/{userID}')
		else:
			redirect("/")

@app.route("/deck/<user_id>", methods=["GET"])
def deckManager(user_id):
	decks = Decks.query.all()
	deck_info = {i.deck_no: i.deck_name.capitalize() for i in decks}
	user_records = Record.query.filter_by(login_id = user_id)
	user_record_info = {i.deck_no: i.last_review for i in user_records}
	return render_template('deck2.html', num = len(deck_info), deck_info = deck_info, user_record_info = user_record_info)


if __name__ == "__main__":
	app.run(debug=True, port=8080)