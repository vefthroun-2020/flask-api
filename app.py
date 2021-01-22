from dataclasses import dataclass
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = '*!69myJ!$Tt&GnaG@iTA&'

db = SQLAlchemy(app)


@dataclass
class Student(db.Model):
    id: int
    name: str
    email: str

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/')
def homepage():
    students = Student.query.all()
    return render_template('homepage.html', students=students)


@app.route('/students')
def students():
    students = Student.query.all()
    return jsonify(students)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'], email=request.form['email'])
        db.session.add(student)
        db.session.commit()
        return redirect('/')
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)
