# CRUD (Create, Read, Update, Delete) API

from dataclasses import dataclass
from flask import Flask, request, redirect, render_template, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beers.sqlite3'
app.config['SECRET_KEY'] = '*!69myJ!$Tt&GnaG@iTA&'

db = SQLAlchemy(app)


@dataclass
class Beer(db.Model):
    id: int
    name: str
    style: str
    recipe: str

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    style = db.Column(db.String(100))
    recipe = db.Column(db.String(100))

    def __init__(self, name, style, recipe):
        self.name = name
        self.style = style
        self.recipe = recipe

# Attempt to create tables
db.create_all()

def do_404():
    # 404 Error - Not found
    response = {
        "message": "Beer was not found",
        "status": 404
    }
    return make_response(response, 404)


@app.route('/beers')
def all_beers():
    # Return all beers
    beers = Beer.query.all()
    return jsonify(beers)


@app.route('/beers/<id>')
def beer_by_id(id):
    # Return beer by ID
    beer = Beer.query.filter_by(id=id).first()
    if beer is None:
        return do_404()
    return jsonify(beer)


@app.route('/beers/new', methods=['PUT'])
def new_beer():
    # Create a new beer
    params = request.json
    beer = Beer(
        name=params['name'],
        style=params['style'],
        recipe=params['recipe']
    )
    db.session.add(beer)
    db.session.commit()

    response = {
        "message": "Beer was added",
    }
    return jsonify(response)


@app.route('/beers/delete/<id>', methods=['DELETE'])
def delete_beer(id):
    # Delete a beer
    beer = Beer.query.filter_by(id=id).first()
    if beer is None:
        return do_404()
    db.session.delete(beer)
    db.session.commit()

    response = {
        "message": "Beer was deleted",
    }
    return jsonify(response)


@app.route('/beers/edit/<id>', methods=['PATCH'])
def edit_beer(id):
    # Edit beer information
    params = request.json

    beer = Beer.query.filter_by(id=id).first()
    if beer is None:
        return do_404()

    # Update the instance and save
    if 'name' in params:
        beer.name = params['name']
    if 'style' in params:
        beer.style = params['style']
    if 'recipe' in params:
        beer.recipe = params['recipe']

    # Save
    db.session.commit()

    return jsonify(beer)


"""
Http Requests Methods
GET - Get information
PUT - Create new items/entries
PATCH - Update existing data
DELETE - To delete data
POST - Execute some task
"""

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
