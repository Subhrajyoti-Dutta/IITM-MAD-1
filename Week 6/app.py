from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Course(db.Model):
	__tablename__ = 'course'
	course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	course_name = db.Column(db.String, nullable=False)
	course_code = db.Column(db.String, nullable=False, unique = True)
	course_description = db.Column(db.String)

class Student(db.Model):
	__tablename__ = 'student'
	student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	roll_number = db.Column(db.String, nullable = False, unique = True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String)

class Enrollment(db.Model):
	__tablename__ = 'enrollment'
	enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable = False)
	course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

app.route("/api/course/{course_id}", methods = ["GET", "POST", "PUT", "DELETE"])
def course_info():
	if request.method == "GET":
		return jsonify(
			course_id= True
		)


if __name__ == "__main__":
	app.run(
		# host = "127.0.0.1",
		# port = 5000,
		debug = True
	)
